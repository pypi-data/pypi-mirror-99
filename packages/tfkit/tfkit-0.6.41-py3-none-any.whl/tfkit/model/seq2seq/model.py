import json
import sys
import os

from transformers import AutoModel
from typing import List

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

import torch
from torch import nn
from tfkit.model.seq2seq.dataloader import get_feature_from_data
from itertools import combinations
from torch.nn.functional import softmax
from math import log
import tfkit.utility.tok as tok
from tfkit.utility.loss import NegativeCElLoss
import numpy as np
import copy


class Model(nn.Module):
    def __init__(self, tokenizer, pretrained, maxlen=512, **kwargs):
        super().__init__()
        self.tokenizer = tokenizer
        if hasattr(pretrained, 'decoder'):
            self.decoder_model = pretrained.decoder
            self.pretrained = pretrained.encoder
            decoder_hidden_size = pretrained.config.hidden_size
        else:
            self.pretrained = pretrained
            decoder_config = copy.deepcopy(pretrained.config)
            decoder_config.is_decoder = True
            decoder_config.add_cross_attention = True
            self.decoder_model = AutoModel.from_config(decoder_config)
            self._tie_encoder_decoder_weights(
                self.pretrained, self.decoder_model,
                self.decoder_model.base_model_prefix
            )
            decoder_hidden_size = decoder_config.hidden_size
        self.model = nn.Linear(decoder_hidden_size, self.tokenizer.__len__())

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.maxlen = maxlen
        print('Using device:', self.device)
        self.decoder_model.to(self.device)
        self.model.to(self.device)
        self.encoder_hidden = None

    def forward(self, batch_data, eval=False, use_prev=False):
        inputs = batch_data['input']
        prevs = batch_data['prev']
        encoder_mask = batch_data['encoder_mask']
        decoder_mask = batch_data['decoder_mask']

        input_tensors = torch.as_tensor(inputs).to(self.device)
        prev_tensors = torch.as_tensor(prevs).to(self.device)
        encoder_mask_tensors = torch.as_tensor(encoder_mask).to(self.device)
        decoder_mask_tensors = torch.as_tensor(decoder_mask).to(self.device)

        if use_prev and self.encoder_hidden is not None:
            encoder_hidden_states = self.encoder_hidden
        else:
            outputs = self.pretrained(input_tensors, attention_mask=encoder_mask_tensors)
            encoder_hidden_states = outputs[0]
            self.encoder_hidden = encoder_hidden_states

        # Decoder
        prediction_output = self.decoder_model(
            input_ids=prev_tensors,
            attention_mask=decoder_mask_tensors,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_mask_tensors
        )[0]
        prediction_scores = self.model(prediction_output)

        if eval:
            result_dict = {
                'label_prob_all': [],
                'label_map': [],
                'prob_list': []
            }
            start = batch_data['start'][0]
            topK = torch.topk(softmax(prediction_scores[0][start], dim=0), 50)
            logit_prob = softmax(prediction_scores[0][start], dim=0).data.tolist()
            prob_result = [(self.tokenizer.convert_ids_to_tokens(id), prob) for prob, id in
                           zip(topK.values.data.tolist(), topK.indices.data.tolist())]
            result_dict['prob_list'].append(logit_prob)
            result_dict['label_prob_all'].append(prob_result)
            result_dict['label_map'].append(prob_result[0])
            outputs = result_dict
        else:
            targets = batch_data['target']
            negative_targets = batch_data['ntarget']
            loss_tensors = torch.as_tensor(targets).to(self.device)
            loss_fct = nn.CrossEntropyLoss(ignore_index=-1)  # -1 index = padding token
            lm_loss = loss_fct(prediction_scores.view(-1, self.tokenizer.__len__()),
                               loss_tensors.view(-1))
            negativeloss_tensors = torch.as_tensor(negative_targets).to(self.device)
            negative_loss_fct = NegativeCElLoss(ignore_index=-1).to(self.device)
            negative_loss = negative_loss_fct(prediction_scores.view(-1, self.tokenizer.__len__()),
                                              negativeloss_tensors.view(-1))
            lm_loss += negative_loss
            outputs = lm_loss
        return outputs

    def _tie_encoder_decoder_weights(self, encoder, decoder, base_model_prefix):
        uninitialized_encoder_weights: List[str] = []
        if decoder.__class__ != encoder.__class__:
            print(
                f"{decoder.__class__} and {encoder.__class__} are not equal. In this case make sure that all encoder weights are correctly initialized."
            )

        def tie_encoder_to_decoder_recursively(
                decoder_pointer: nn.Module,
                encoder_pointer: nn.Module,
                module_name: str,
                uninitialized_encoder_weights: List[str],
                depth=0,
        ):
            assert isinstance(decoder_pointer, nn.Module) and isinstance(
                encoder_pointer, nn.Module
            ), f"{decoder_pointer} and {encoder_pointer} have to be of type torch.nn.Module"
            if hasattr(decoder_pointer, "weight"):
                assert hasattr(encoder_pointer, "weight")
                encoder_pointer.weight = decoder_pointer.weight
                if hasattr(decoder_pointer, "bias"):
                    assert hasattr(encoder_pointer, "bias")
                    encoder_pointer.bias = decoder_pointer.bias
                return

            encoder_modules = encoder_pointer._modules
            decoder_modules = decoder_pointer._modules
            if len(decoder_modules) > 0:
                assert (
                        len(encoder_modules) > 0
                ), f"Encoder module {encoder_pointer} does not match decoder module {decoder_pointer}"

                all_encoder_weights = set([module_name + "/" + sub_name for sub_name in encoder_modules.keys()])
                encoder_layer_pos = 0
                for name, module in decoder_modules.items():
                    if name.isdigit():
                        encoder_name = str(int(name) + encoder_layer_pos)
                        decoder_name = name
                        if not isinstance(decoder_modules[decoder_name], type(encoder_modules[encoder_name])) and len(
                                encoder_modules
                        ) != len(decoder_modules):
                            # this can happen if the name corresponds to the position in a list module list of layers
                            # in this case the decoder has added a cross-attention that the encoder does not have
                            # thus skip this step and subtract one layer pos from encoder
                            encoder_layer_pos -= 1
                            continue
                    elif name not in encoder_modules:
                        continue
                    elif depth > 500:
                        raise ValueError(
                            "Max depth of recursive function `tie_encoder_to_decoder` reached. It seems that there is a circular dependency between two or more `nn.Modules` of your model."
                        )
                    else:
                        decoder_name = encoder_name = name
                    tie_encoder_to_decoder_recursively(
                        decoder_modules[decoder_name],
                        encoder_modules[encoder_name],
                        module_name + "/" + name,
                        uninitialized_encoder_weights,
                        depth=depth + 1,
                    )
                    all_encoder_weights.remove(module_name + "/" + encoder_name)

                uninitialized_encoder_weights += list(all_encoder_weights)

        # tie weights recursively
        tie_encoder_to_decoder_recursively(decoder, encoder, base_model_prefix, uninitialized_encoder_weights)
        if len(uninitialized_encoder_weights) > 0:
            print(
                f"The following encoder weights were not tied to the decoder {uninitialized_encoder_weights}"
            )
        else:
            print("All encoder weights tied to the decoder")

    def _jaccard_similarity(self, list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        return len(s1.intersection(s2)) / len(s1.union(s2))

    def _isSimilar(self, s, t):
        return self._jaccard_similarity(s, t) > 0.5

    def _filterSimilar(self, d, topP):
        while True:
            filteredOne = False
            for s, t in combinations(d, 2):
                if self._isSimilar(s[0], t[0]) and len(d) - 1 >= topP:
                    d.remove(t)
                    filteredOne = True
                    break
            if not filteredOne:
                break

    def predict(self, input='', topK=1, topP=0.85, mode=['greedy', 'topK', 'topP'], decodenum=1, filtersim=True,
                reserved_len=0, task=None, handle_exceed='start_slice'):
        filtersim = json.loads(str(filtersim).lower())
        topK = int(topK)
        topP = float(topP)
        decodenum = int(decodenum)
        mode = mode[0] if isinstance(mode, list) else mode.lower()

        self.eval()
        sequences = [[[], 1.0]]
        with torch.no_grad():
            while True:
                all_candidates = list()
                exceed = False
                for seq in sequences:
                    if tok.tok_sep(self.tokenizer) not in seq[0]:
                        tokens, score = seq
                        feature_dict = get_feature_from_data(self.tokenizer, self.maxlen, input, tokens,
                                                             reserved_len=reserved_len,
                                                             handle_exceed=handle_exceed)[-1]
                        # check input exceed
                        if len(tokens) >= self.maxlen or feature_dict['start'] >= self.maxlen:
                            exceed = True
                            all_candidates.append(seq)
                            continue

                        for k, v in feature_dict.items():
                            feature_dict[k] = [v]
                        predictions = self.forward(feature_dict, eval=True, use_prev=True)
                        token_prob_list = predictions['label_prob_all'][0]
                        # topK topP
                        if 'top' in mode:
                            prob_list = [prob for _, prob in token_prob_list]
                            if 'topk' in mode:
                                sample_list = prob_list[:topK]
                                decode_range = max(decodenum, topK)
                                prob_norm = [float(i) / sum(sample_list) for i in sample_list]
                                choice_list = np.random.choice(sample_list, p=prob_norm,
                                                               size=decode_range,
                                                               replace=False)
                            else:
                                topP_list = np.cumsum(prob_list)
                                index_overP = [i for i, x in enumerate(topP_list) if x > topP]
                                index_overP = 0 if len(index_overP) < 1 else index_overP[0]
                                sample_list = prob_list[:index_overP + 1]
                                prob_norm = [float(i) / sum(sample_list) for i in sample_list]
                                choice_list = np.random.choice(sample_list, p=prob_norm,
                                                               size=decodenum)
                            for idx in range(decodenum):
                                sampling_index = prob_list.index(choice_list[idx])
                                k, v = token_prob_list[sampling_index]
                                candidate = [tokens + [k], score + -log(v)]
                                all_candidates.append(candidate)

                        # greedy / beam search
                        else:
                            for k, v in token_prob_list[:50]:
                                if len(tokens) > 0 and tokens[-1] == k or len(k) < 1:
                                    continue
                                candidate = [tokens + [k], score + -log(v)]
                                all_candidates.append(candidate)
                    else:
                        all_candidates.append(seq)

                ordered = sorted(all_candidates, key=lambda tup: tup[1])
                if filtersim:
                    self._filterSimilar(ordered, decodenum)
                sequences = ordered[:decodenum]
                stop = 0
                for i in sequences:
                    # i[0] - sequence,i[1] - sequence score
                    if tok.tok_sep(self.tokenizer) in i[0] or i[1] > self.maxlen:
                        stop += 1
                if stop == len(sequences) or exceed:
                    break

            for i in range(len(sequences)):
                if tok.tok_sep(self.tokenizer) in sequences[i][0]:  # remove sep token
                    sequences[i][0] = sequences[i][0][:sequences[i][0].index(tok.tok_sep(self.tokenizer))]
                sequences[i][0] = self.tokenizer.convert_tokens_to_string(sequences[i][0])

            result_dict = {
                'label_map': sequences
            }
            self.encoder_hidden = None
            return [i[0] for i in sequences], [result_dict]

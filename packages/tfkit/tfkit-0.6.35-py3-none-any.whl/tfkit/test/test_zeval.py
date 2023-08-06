import unittest

import os

import tfkit


class TestEval(unittest.TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../../"))
    DATASET_DIR = os.path.join(ROOT_DIR, 'demo_data')
    ONEBYONE_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/onebyone/2.pt')
    ONCE_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/once/2.pt')
    ONCECTC_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/oncectc/30.pt')
    SEQ2SEQ_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/seq2seq/10.pt')
    CLM_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/clm/20.pt')
    CLAS_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/clas/2.pt')
    MASK_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/mask/2.pt')
    MCQ_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/mcq/2.pt')
    TAG_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/tag/2.pt')
    QA_MODEL_PATH = os.path.join(ROOT_DIR, 'tfkit/test/cache/qa/2.pt')
    TAG_DATASET = os.path.join(DATASET_DIR, 'tag_row.csv')
    CLAS_DATASET = os.path.join(DATASET_DIR, 'classification.csv')
    GEN_DATASET = os.path.join(DATASET_DIR, 'generate.csv')
    SEQ2SEQ_DATASET = os.path.join(DATASET_DIR, 'gen_eng.csv')
    MASK_DATASET = os.path.join(DATASET_DIR, 'mask.csv')
    MCQ_DATASET = os.path.join(DATASET_DIR, 'mcq.csv')
    QA_DATASET = os.path.join(DATASET_DIR, 'qa.csv')
    ADDED_TOK_MODEL = os.path.join(ROOT_DIR, 'tfkit/test/cache/voidful/albert_chinese_tiny_added_tok')

    def testHelp(self):
        result = os.system('tfkit-eval -h')
        self.assertTrue(result == 0)

    def test_parser(self):
        parser, _ = tfkit.eval.parse_eval_args(
            ['--model', 'onebyone', '--metric', 'emf1', '--valid', 'test.csv', '--print'])
        print(parser)
        self.assertTrue(parser.get('model') == 'onebyone')

        eval_parser, model_parser = tfkit.eval.parse_eval_args(
            ['--model', 'onebyone', '--metric', 'emf1', '--valid', 'test.csv', '--print', '--decodenum', '2'])
        self.assertTrue(eval_parser.get('model') == 'onebyone')
        self.assertTrue(model_parser.get('decodenum') == '2')

    def testEvalGen(self):
        tfkit.eval.main(
            ['--model', self.ONEBYONE_MODEL_PATH, '--valid', self.GEN_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.ONEBYONE_MODEL_PATH + ' --valid ' + self.GEN_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalGenOnce(self):
        tfkit.eval.main(
            ['--model', self.ONCE_MODEL_PATH, '--valid', self.GEN_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.ONCE_MODEL_PATH + ' --valid ' + self.GEN_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalGenOnceCTC(self):
        tfkit.eval.main(
            ['--model', self.ONCECTC_MODEL_PATH, '--valid', self.SEQ2SEQ_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.ONCECTC_MODEL_PATH + ' --valid ' + self.SEQ2SEQ_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalSeq2Seq(self):
        tfkit.eval.main(
            ['--model', self.SEQ2SEQ_MODEL_PATH, '--valid', self.SEQ2SEQ_DATASET, '--metric', 'emf1', '--print',
             '--decodenum', '2'])
        tfkit.eval.main(
            ['--model', self.SEQ2SEQ_MODEL_PATH, '--valid', self.SEQ2SEQ_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.SEQ2SEQ_MODEL_PATH + ' --valid ' + self.SEQ2SEQ_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalCLM(self):
        tfkit.eval.main(
            ['--model', self.CLM_MODEL_PATH, '--valid', self.SEQ2SEQ_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.CLM_MODEL_PATH + ' --valid ' + self.SEQ2SEQ_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalMask(self):
        tfkit.eval.main(
            ['--model', self.MASK_MODEL_PATH, '--valid', self.MASK_DATASET, '--metric', 'clas', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.MASK_MODEL_PATH + ' --valid ' + self.MASK_DATASET + ' --metric clas --print')
        self.assertTrue(result == 0)

    def testEvalMCQ(self):
        tfkit.eval.main(
            ['--model', self.MCQ_MODEL_PATH, '--valid', self.MCQ_DATASET, '--metric', 'clas', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.MCQ_MODEL_PATH + ' --valid ' + self.MCQ_DATASET + ' --metric clas --print')
        self.assertTrue(result == 0)

    def testEvalQA(self):
        tfkit.eval.main(
            ['--model', self.QA_MODEL_PATH, '--valid', self.QA_DATASET, '--metric', 'emf1', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.QA_MODEL_PATH + ' --valid ' + self.QA_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

    def testEvalClassify(self):
        tfkit.eval.main(
            ['--model', self.CLAS_MODEL_PATH, '--valid', self.CLAS_DATASET, '--metric', 'clas', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.CLAS_MODEL_PATH + ' --valid ' + self.CLAS_DATASET + ' --metric clas --print')
        self.assertTrue(result == 0)

    def testEvalTag(self):
        tfkit.eval.main(
            ['--model', self.TAG_MODEL_PATH, '--valid', self.TAG_DATASET, '--metric', 'clas', '--print'])
        result = os.system(
            'tfkit-eval --model ' + self.TAG_MODEL_PATH + ' --valid ' + self.TAG_DATASET + ' --metric clas --print')
        self.assertTrue(result == 0)

    def testEvalAddedTokenModel(self):
        result = os.system(
            'tfkit-eval --model ' + self.ONEBYONE_MODEL_PATH + ' --valid ' + self.GEN_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)
        result = os.system(
            'tfkit-eval --model ' + self.ONEBYONE_MODEL_PATH + ' --config ' + self.ADDED_TOK_MODEL + ' --valid ' + self.GEN_DATASET + ' --metric emf1 --print')
        self.assertTrue(result == 0)

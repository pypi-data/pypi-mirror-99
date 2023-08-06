from treform.spelling import *
import treform
from treform.spelling.config import KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR, \
    KO_WIKIPEDIA_ORG_TRAIN_SENTENCES_FILE, KO_WIKIPEDIA_ORG_VALID_SENTENCES_FILE, KO_WIKIPEDIA_ORG_TEST_SENTENCES_FILE, KO_WIKIPEDIA_ORG_CHARACTERS_FILE, \
    KO_WIKIPEDIA_ORG_DIR

import os

from treform.utility.dataset import DataSet
from treform.utility.num_util import NumUtil
from treform.utility.char_one_hot_vector import CharOneHotVector
from treform.utility.datafile_util import DataFileUtil
from treform.spelling.spelling_error_correction import SpellingErrorCorrection
import tensorflow.compat.v1 as tf

class BaseSpellingCorrector:
    IN_TYPE = [str]
    OUT_TYPE = [str]

class DAESpellingCorrector(BaseSpellingCorrector):
    IN_TYPE = [str]
    OUT_TYPE = [str]

    def __init__(self):
        self.window_size = 10
        characters_file = KO_WIKIPEDIA_ORG_CHARACTERS_FILE
        #D:\python_workspace\treform\treform\spelling\models\spelling_error_correction\spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100
        self.model_file = os.path.join(KO_WIKIPEDIA_ORG_SPELLING_ERROR_CORRECTION_MODEL_DIR,
                                    'spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100')

        self.features_vector = CharOneHotVector(DataFileUtil.read_list(characters_file))
        labels_vector = CharOneHotVector(DataFileUtil.read_list(characters_file))
        self.n_features = len(self.features_vector) * self.window_size  # number of features
        n_classes = len(labels_vector) * self.window_size
        self.total_epoch = 5
        self.features_vector_size = self.n_features // self.window_size

    def __call__(self, *args, **kwargs):
        model_path = "D:\\python_workspace\\treform\\treform\\spelling\\models\\spelling_error_correction\\spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100\\model"
        detection_graph = tf.Graph()

        with tf.Session(graph=detection_graph) as sess:
            # Load the graph with the trained states
            loader = tf.train.import_meta_graph('D:\\python_workspace\\treform\\treform\\spelling\\models\\spelling_error_correction\\spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100\\model.meta')
            loader.restore(sess, model_path)

            # Get the tensors by their variable name
            # Make predictions
            dropout_keep_rate = 1.0

            dropout_keep_prob = tf.placeholder(tf.float32)
            X = detection_graph.get_tensor_by_name('X:0')  # shape=(batch_size, window_size * feature_vector.size)
            Y = detection_graph.get_tensor_by_name('Y:0')
            W1 = detection_graph.get_tensor_by_name('W1:0')
            b1 = detection_graph.get_tensor_by_name('b1:0')
            layer1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1, name='layer1')
            layer1_dropout = tf.nn.dropout(layer1, dropout_keep_prob, name='layer1_dropout')

            #vals = tf.train.list_variables(tf.train.latest_checkpoint('D:\\python_workspace\\treform\\treform\\spelling\\models\\spelling_error_correction\\spelling_error_correction_model.sentences=3.window_size=10.noise_rate=0.1.n_hidden=100\\'))
            #print(vals)
            #op = sess.graph.get_operations()
            #for m in op:
            #    print(m)

            noised_sentence = SpellingErrorCorrection.encode_noise(args[0], noise_rate=0.1)
            denoised_sentence = noised_sentence[:]  # will be changed with predict
            for start in range(0, len(noised_sentence) - self.window_size + 1):
                chars = denoised_sentence[start: start + self.window_size]
                original_chars = args[0][start: start + self.window_size]
                _features = [chars]
                _labels = [original_chars]

                dataset = DataSet(features=_features, labels=_labels, features_vector=self.features_vector,
                                  labels_vector=self.features_vector)
                dataset.convert_to_one_hot_vector()
                try:
                    _y_hat, _cost, _accuracy = sess.run(['y_hat:0', 'cost:0', 'accuracy:0'],
                                                        feed_dict={X: dataset.features, Y: dataset.labels,
                                                                   dropout_keep_prob: dropout_keep_rate})

                    y_hats = [self.features_vector.to_values(_l) for _l in _y_hat]
                    #if _features[0] == y_hats[0]:
                    #    print('same   : "%s"' % (_features[0]))
                    #else:
                    #    print('denoise: "%s" -> "%s"' % (_features[0], y_hats[0]))
                    denoised_sentence = denoised_sentence.replace(_features[0], y_hats[0])
                except:
                    print('"%s"%s "%s"%s' % (chars, dataset.features.shape, original_chars, dataset.labels.shape))

                #print(denoised_sentence)

        return denoised_sentence

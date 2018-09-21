# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Runs a trained audio graph against a WAVE file and reports the results.

The model, labels and .wav file specified in the arguments will be loaded, and
then the predictions from running the model against the audio data will be
printed to the console. This is a useful script for sanity checking trained
models, and as an example of how to use an audio model from Python.

Here's an example of running it:

python tensorflow/examples/speech_commands/label_wav.py \
--graph=/tmp/my_frozen_graph.pb \
--labels=/tmp/speech_commands_train/conv_labels.txt \
--wav=/tmp/speech_dataset/left/a5d485dc_nohash_0.wav

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# pylint: disable=unused-import
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
# pylint: enable=unused-import

FLAGS = None


def load_graph(filename):
	"""Unpersists graph from file as default graph."""
	with tf.gfile.FastGFile(filename, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def, name='')



def run_graph(wav_data, input_layer_name, output_layer_name):
	"""Runs the audio data through the graph and prints predictions."""
	with tf.Session() as sess:
		# Feed the audio data as input to the graph.
		#   predictions  will contain a two-dimensional array, where one
		#   dimension represents the input image count, and the other has
		#   predictions per class
		softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
		predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})
		# Sort to show labels in order of confidence
		top_k = predictions.argsort()[-3:][::-1]
		print(top_k[0])
		return top_k[0]


def label_wav():
	"""Loads the model and labels, and runs the inference to print predictions."""
	#if not wav or not tf.gfile.Exists(wav):
		#tf.logging.fatal('Audio file does not exist %s', wav)

	# load graph, which is stored in the default session
	graph='./models/new1.pb'
	input_name='wav_data:0'
	output_name='labels_softmax:0'
	load_graph(graph)
	wave="./utils/words/record.wav"
	with open(wave, 'rb') as wav_file:
			wav_data = wav_file.read()
	word=run_graph(wav_data, input_name, output_name)
	names=['unknown','silence','laddu','modak','pedha']
	return names[word]


def main(_):
	"""Entry point for script, converts flags to arguments."""
	label_wav()

if __name__ == '__main__':
	main(0)
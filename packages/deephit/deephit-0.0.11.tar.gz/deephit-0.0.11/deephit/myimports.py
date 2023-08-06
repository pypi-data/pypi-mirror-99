import numpy as np 
import pandas as pd 
import tensorflow as tf 
from tensorflow.contrib.layers import fully_connected as FC_Net 
from sklearn.metrics import brier_score_loss 
from sklearn.model_selection import train_test_split 
import random 
from lifelines import KaplanMeierFitter 

import matplotlib.pyplot as plt 
import math 
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder

import sklearn.metrics as metrics

import datetime

from termcolor import colored
import importlib

from scipy import stats
import math
import os
import sys
import numpy as np
import tensorflow as tf
from scipy.io.wavfile import write
from lib.model import CVAE as Model
from lib.latent_chord_class import latent_chord
from lib.specgrams_helper import SpecgramsHelper


    
def main():
    
    ######SELECT HERE PATH OF TRAINED MODEL AND LATENT DIMENTION OF TRAINED MODEL (THEY MUST MATCH)#######
    trained_model_path = './trained_models/2019_10_25/14_54_03mel_p0_latent_2_lr_3e-05_b_1_se_1_ee_501_ep_385'
    latent_dim = 2

    ######               WRITE HERE A LIST WITH THE SAMPLE POINTS             ########### 
    ######EACH SAMPLE POINTNEEDS TO HAVE SAME NUMBER OF ELEMENTS AS latent_dim###########
    sample_points = [[7, 8],[18,-18],[18,-7],[7,-30],[39,-10],[17,10]]
    chord_saving_path = './generated_chords/'
    
    
    
    if not os.path.exists(chord_saving_path):
        os.makedirs(chord_saving_path)
    
    spec_helper = SpecgramsHelper(audio_length=64000,
                           spec_shape=(128, 1024),
                           overlap=0.75,
                           sample_rate=16000,
                           mel_downscale=1)
   

    model = Model(latent_dim)
    print('\n\nLoading Trained Model...')
    model.load_weights(trained_model_path)
    print('Success Loading Trained Model!\n')
    
    n = 1
    for sample_point in sample_points:
        chord = latent_chord(tf.constant([sample_point], dtype='float32'),model,spec_helper)
        write(chord_saving_path+'chord'+str(n)+'.wav', data = chord.audio, rate = 16000)
        print('Chord '+str(n)+' generated!')
        n += 1
    print('\n\nSUCCESS: ALL CHORDS GENERATED!    (chords are saved at '+chord_saving_path+')')
             
    
if __name__ == '__main__':
    main()
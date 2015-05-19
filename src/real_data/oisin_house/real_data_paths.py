import os
import yaml
import socket
import system_setup
from copy import deepcopy

host_name = socket.gethostname()
print host_name

if host_name == 'troll' or host_name == 'biryani':
    data_folder = '/media/ssd/data/oisin_house/'
    converter_path = ''
else:
    data_folder = '/Users/Michael/projects/shape_sharing/data/oisin_house/'
    converter_path = '/Users/Michael/projects/InfiniTAM_Alt/convertor/voxels_to_ply.py'

raw_data = data_folder + 'data2/'

scene_names = [o
          for o in os.listdir(raw_data)
          if os.path.isdir(os.path.join(raw_data,o))]

# scene_names = ['saved_aaron']

scenes = [{'folder':raw_data,
           'scene':scene}
           for scene in scene_names]

yaml_train_location = data_folder + 'train_test/train.yaml'
yaml_train_location2 = data_folder + 'train_test/train2.yaml'
yaml_test_location = data_folder + 'train_test/test.yaml'

with open(yaml_train_location, 'r') as f:
    temp_train_data = yaml.load(f)

with open(yaml_train_location2, 'r') as f:
    temp_train_data2 = yaml.load(f)

all_train_data = temp_train_data + temp_train_data2


with open(yaml_test_location, 'r') as f:
    test_data = yaml.load(f)

test_data = test_data[:system_setup.max_test_sequences]

if system_setup.small_sample:
    all_train_data = all_train_data[:system_setup.max_sequences]



sequences = []
for t in scenes:
    t['folder'] = raw_data
    fpath = t['folder'] + t['scene'] + '/test_frame.txt'

    with open(fpath, 'r') as f:
        frames = [int(l) for l in f]

    temp = []
    for fr in frames:
        this_t = deepcopy(t)
        this_t['frames'] = [fr]
        this_t['name'] = this_t['scene'] + '_' + str(this_t['frames'])
        temp.append(this_t)

    sequences.append(temp)

# saving...
models_folder = data_folder + 'models/%s/'

# voxlets_dict_data_path = models_folder + 'dictionary/dict_data/'
voxlets_dictionary_path = models_folder + 'dictionary/'
voxlets_data_path = models_folder + 'training_voxlets/'
voxlet_model_path = models_folder + 'model_%s.pkl'

# this is where to save the voxlets used for testing the models
evaluation_data_path = models_folder + 'model_evaluation_voxlets/'


# voxlet_prediction_image_path = base_path + "/voxlets/bigbird/predictions/%s/%s_%s.png"
voxlet_prediction_img_path = data_folder + '/predictions/%s/%s/%s.png'

# first %s is the test batch category name, second is the sequence name
prediction_folderpath = data_folder + '/predictions/%s/%s/pickles/'

scores_path = data_folder + '/predictions/%s/%s/scores.yaml'

# final %s is the actual test being done
prediction_path = data_folder + '/predictions/%s/%s/%s.pkl'


def new_dropbox_dir():
    '''
    creates a new dropbox directory for results
    '''
    base_path = \
        os.path.expanduser('~/Dropbox/PhD/Projects/Shape_sharing_data/oisin_house_predictions/res_%04d/')
    count = 0
    while os.path.exists(base_path % count):
        count += 1
    os.mkdir(base_path % count)
    assert os.path.exists(base_path % count)
    return base_path % count

# **Extract Openface features for given dataset**
Extracts openface features like gaze, headpose, lms, AUS etc along with aligned faces [[1](#1)][[2](#2)].

## **Openface docker installation**

### *Run the below commands in your terminal*
1. If you have not installed docker, install from [here](https://docs.docker.com/docker-for-mac/install/).

2. Pull openface from docker hub. This image is around 8gb.
```bash
docker pull algebr/openface
```

3. Check if docker image is present.
```bash
docker images -a
```
4. Run the openface docker process.
```bash
docker run -it --rm --name openface algebr/openface
```
* `-it` interactive
* `--rm` remove instance after killing the process
* `--name` name of the image file manually assigned

5. Check if the openface docker process is running.
```bash
docker ps -a
```

## **Installation**

1. Install `pip` packages

```bash
pip install -r requirements.txt
```

2. Create an `output/dataset_name` folder in the main repo.

## **Extract**

```bash
python main.py extract --config path_to_yaml_config
```

## **Configurations**

All the configurations are present in the path `./configs/`. Your dataset folder structures needs to be specified in the config file for the program to extract accordingly. \
For example, *type*, *ext* are the parameters defining your folder structure. Create your own config file in the same format for any new dataset.

## **References**
<a id="1">[1]</a>
T. Baltrusaitis, A. Zadeh, Y. C. Lim and L. Morency, "OpenFace 2.0: Facial Behavior Analysis Toolkit," 2018 13th IEEE International Conference on Automatic Face & Gesture Recognition (FG 2018), Xi'an, 2018, pp. 59-66, doi: 10.1109/FG.2018.00019.

<a id="2">[2]</a>
https://github.com/TadasBaltrusaitis/OpenFace


# determine-docker-tags

A python program used to determine which docker tags should be applied to a docker image depending on various factors. This is mainly intended to be used together with Drone CI to automatically figure out version tags before building a container image.

## Installation

As this is mainly intended to be used with Drone CI there is a ready to go docker image on [Docker Hub](https://hub.docker.com/r/mwalbeck/determine-docker-tags). You can also find the source for the docker image [here](https://git.walbeck.it/walbeck-it/docker-determine-docker-tags).

If you're not interested in a docker image you can also find it on [PyPi](https://pypi.org/project/determine-docker-tags/) and it can easily be installed with:

```
pip install determine-docker-tags
```

## Options

Here is a list of the options available. You can find more detailed usage instructions below.

| ENV Var         | Default      | Description                                                                                                                                                                                          |
| --------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VERSION_TYPE    | ""           | How the program should find the version number. Can be "docker_env", "docker_from", "date" or "".                                                                                                    |
| APP_NAME        | ""           | The name of the application whose version number you want to use to generate tags.                                                                                                                   |
| DOCKERFILE_PATH | "Dockerfile" | The path to the Dockerfile you want to run the program on                                                                                                                                            |
| APP_ENV         | ""           | A static string to add to the end of every tag with a "-" added inbetween the tag and the string. The string will not be added to any tags defined in CUSTOM_TAGS.                                   |
| CUSTOM_TAGS     | ""           | Any extra static tags you want to add to the image, for example "latest". You can provide a list in the form of a comma separated string to specify multiple tags. For example "latest,prod,example" |
| INCLUDE_MAJOR   | "yes"        | If the major version number should be a tag. This setting will be ignored if the major version number is 0. Can be "yes" or "no".                                                                    |
| INCLUDE_SUFFIX  | "yes"        | If the suffix that you find after the version number in many docker image tags should be kept and added to every tag. Can be "yes" or "no"                                                           |

## Usage

The program is configured through environment variables. You can see the different options below. The program automatically figures out the version numbers to use as tags from a Dockerfile. The tags are put into a .tags file in the current workspace to be picked up by the drone docker plugin. This program is mainly intended to handle SemVer and may or may not work well with other versioning styles.

### Version type

To use the program you first need to figure out which `VERSION_TYPE` you want to use. There are four options to choose from. The default or an empty string requires `CUSTOM_TAGS` to be set and just creates a .tags file with the contents of `CUSTOM_TAGS`.

#### date

If `VERSION_TYPE` is set to `date` a tag will be created corresponding to the current date in format `YEARMONTHDAY` for example `20210101`. If `APP_ENV` is set it will currently be ignored using this `VERSION_TYPE`.

#### docker_env

If `VERSION_TYPE` is set to `docker_env` then `APP_NAME` is also required. When `docker_env` is used the program looks for the `APP_NAME` version number set as an ENV var in the Dockerfile. The required formating to use in the Dockerfile is:

```
ENV APP_NAME_VERSION VERSION_NUMBER
```

So lets say the "APP_NAME" we are looking for is Nginx, then we would set "APP_NAME" to "NGINX" and the ENV var in the Dockerfile would look like this:

```
ENV NGINX_VERSION 1.18.0
```

This would generate the following tags:

```
1,1.18,1.18.0
```

#### docker_from

If `VERSION_TYPE` is set to `docker_from` then `APP_NAME` is also required. When using this `VERSION_TYPE` the version number is taken from a `FROM` instruction in the provided Dockerfile. Let's say we had the following `FROM` instruction in our Dockerfile:

```
FROM nginx:1.18.0
```

We then set `APP_NAME` to `nginx` and the generated tags would be:

```
1,1.18,1.18.0
```

### APP ENV

`APP_ENV` is a static string that will be added to the end of dynamically created tag, so not the ones defined in `CUSTOM_TAGS`. A `-` is added between the generated tag and the contents of `APP_ENV`. Let's say we had the version number `1.18.0` and `APP_ENV` was set to `prod` then we would get the following tags:

```
1-prod,1.18-prod,1.18.0-prod
```

### INCLUDE_MAJOR

`INCLUDE_MAJOR` determine whether or not the major version number should have a tag of its own. The default for this option is `yes` If the major version number is `0` this option will be ignored and a tag with only the major version number won't be created. Let's say we had the version number `1.18.0` and `INCLUDE_MAJOR` is set to `no` then we would get the following tags:

```
1.18,1.18.0
```

### INCLUDE_SUFFIX

`INCLUDE_SUFFIX` is mainly intended to be used with the `docker_from` version type. It determines whether or not the suffix should be included in the generated tags. The default for this option is `yes`. Let's say we had the following `FROM` instruction in our Dockerfile:

```
FROM nginx:1.18.0-alpine
```

With the default of `yes` that would generated the following tags:

```
1-alpine,1.18-alpine,1.18.0-alpine
```

And if set to `no` the following tags would be generated:

```
1,1.18,1.18.0
```

## License

This program is licensed under the GPLv3 or later.

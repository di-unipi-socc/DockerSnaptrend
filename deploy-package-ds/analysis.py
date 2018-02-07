import requests
import datetime

def analysis(json_image, context):
    # docker_hub_endpoint="https://hub.docker.com"

    logger = context['logger']
    client_images = context['images']

    logger.info("{} received.".format(json_image['name']))

    name = json_image['name']

    stars = json_image.pop('star_count', None)
    pulls = json_image.pop('pull_count', None)
    last_updated = json_image.pop('last_updated', None)

    logger.debug("pulls: {} stars:{} Last updated: {}".format(stars,pulls,last_updated))
    date_now = str(datetime.datetime.now())

    try:
        if(client_images.is_new(name)):
            logger.info("{} is new to local storage".format(name))
            image_with_pulls_stars_updated = {**json_image,
                            'pulls': [{"date_scan":date_now,"pulls":pulls}],
                            "stars":[{"date_scan":date_now, "stars":stars}],
                            "last_updated":[{"date_scan":date_now, "last_updated":last_updated}],
                            }
            client_images.post_image(image_with_pulls_stars_updated)
            logger.debug("{} inserted into the local database".format(name))
            return True
        else:
            local_json_image = client_images.get_image(name)
            local_json_image['pulls'].append({"date_scan":date_now,"pulls":pulls})
            local_json_image['stars'].append({"date_scan":date_now,"stars":stars})
            local_json_image['last_updated'].append({"date_scan":date_now,"last_updated":last_updated})
            client_images.put_image(local_json_image)
            logger.info("{} updated the #stars,#pulls,#last updated into database".format(name))
            return True
    except ImageNotFound as e:
        self.logger.exception(str(e))
        return False
    except requests.exceptions.ConnectionError as e:
        self.logger.exception("ConnectionError: " )
        return False
    except:
        self.logger.exception("Unexpected error:")
        return False
    # {"star_count": 107,
    # "pull_count": 1430790,
    # "repo_owner": None,
    # "short_description": "",
    #  "is_automated": True,
    #  "is_official": False,
    #  "repo_name": "sameersbn/postgresql",
    #  "tag": "9.4-17",
    #  "name": "sameersbn/postgresql:9.4-17",
    #  "full_size": 81978718,
    #  "images": [{"size": 81978718}], "id": 2384003,
    #  "repository": 14080, "creator": 3263,
    #  "last_updater": 3263,
    #  "last_updated": "2016-03-22T06:46:03.447956Z",
    #  "image_id": None, "v2": True}
    #  }

    # return True

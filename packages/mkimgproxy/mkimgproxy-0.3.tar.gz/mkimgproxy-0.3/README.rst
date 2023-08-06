############
mkimgproxy
############

Generates URL for imgproxy image processing server

Use following command line to generate IMGPROXY_KEY and IMGPROXY_SALT

.. code:: bash

    echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')

.. code:: python

    from mkimgproxy import ImgProxy

    IMGPROXY_URL = "http://my-imgproxy-server/path"
    IMGPROXY_KEY = "9cbc4f564037858e5b9f2304f8540aa606943bddeaecb00a0b4a498092d0d65c079e291d3a2ddceafd23f1a29bb914fbf91a8464515826bb6a9f609800781182"
    IMGPROXY_SALT = "3dae9fbe7138431c57d59625d19175901df23786b1b8b6c65a39a0ac26f344809478bb3c7f6a838a1a45dbe123f85a16d8ce74c2f595cbf61d12a8470c588201"

    imgProxy = ImgProxy(IMGPROXY_KEY, IMGPROXY_SALT, IMGPROXY_URL)
    resizedImageUrl = imgProxy.generate("http://example.com/images/curiosity.jpg", {
        "s": "800:500", "rt": "fit", "g": "sm", "q": 70, "sm": "true"}, "jpeg")

    print(resizedImageUrl)
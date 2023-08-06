# Django docker entrypoint

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

    docker build -t ${DJANGO_DOCKER_IMAGE} . && docker run --env DJANGO_DEBUG=True ${DJANGO_DOCKER_IMAGE}

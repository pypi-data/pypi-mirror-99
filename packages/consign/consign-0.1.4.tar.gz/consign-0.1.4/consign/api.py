from . import sessions


def consign(method, data, path, **kwargs):
    '''Constructs and sends a :class:`Request <Request>`.
    :param method: method for the new :class:`Consign` object: ``CSV``, etc.
    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    :param delimiter: delimiter used to separate elements in a CSV row.
    '''
    # By using the 'with' statement we are sure the session is closed, thus we
    # avoid leaving sockets open which can trigger a ResourceWarning in some
    # cases, and look like a memory leak in others.
    with sessions.Session() as session:
        return session.consign(method=method, data=data, path=path, **kwargs)


def csv(data, path, **kwargs):
    r'''Stores a CSV file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('csv', data, path, **kwargs)


def json(data, path, **kwargs):
    r'''Stores a JSON file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('json', data, path, **kwargs)


def txt(data, path, **kwargs):
    r'''Stores a TXT file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('txt', data, path, **kwargs)


def html(data, path, **kwargs):
    r'''Stores a HTML file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('html', data, path, **kwargs)


def pdf(data, path, **kwargs):
    r'''Stores a PDF file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('pdf', data, path, **kwargs)


def img(data, path, **kwargs):
    r'''Stores an image locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('img', data, path, **kwargs)


def blob(data, path, **kwargs):
    r'''Stores a PDF file locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('blob', data, path, **kwargs)


def table(data, path, **kwargs):
    r'''Stores an image locally.

    :param data: data for the new :class:`Consign` object.
    :param path: path for the new :class:`Consign` object.
    '''
    return consign('table', data, path, **kwargs)

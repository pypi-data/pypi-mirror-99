import io
import gzip
from xialib.decoder import Decoder


class BasicDecoder(Decoder):
    """
    Supported data encodes: ``blob``, ``flat``, ``gzip``, ``b64g``
    """
    supported_encodes = ['blob', 'flat', 'gzip', 'b64g']

    def _encode_to_blob(self, data_or_io, from_encode, **kwargs):
        if isinstance(data_or_io, io.IOBase):
            if from_encode == 'blob':
                yield data_or_io
            elif from_encode == 'gzip':
                with gzip.GzipFile(fileobj=data_or_io) as f:
                    yield f
            else:
                # flat or b64g, terminating IO
                data_or_io = data_or_io.read().decode()
                for output in self.basic_encoder(data_or_io, from_encode, 'blob'):
                    yield output
        else:
            for output in self.basic_encoder(data_or_io, from_encode, 'blob'):
                yield output

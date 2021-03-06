import pyrox.filtering as filtering


class CryptoFilter(filtering.HttpFilter):
    """
    This filter encrypts/decrypts data streamed through it on its way
    to/from a Swift encrypted volume.
    """

    def __init__(self):
        super(CryptoFilter, self).__init__()
        #self.buffer_mgr = BufferManager(processor=SampleCryptoProcessor(is_encrypt=True))
        self.processor = SampleCryptoProcessor(is_encrypt=True)

    @filtering.handles_request_head
    def on_request_head(self, request_head):
        print(">>>>>>> {}".format(self))
        print('Got request head with verb: {}'.format(request_head.method))

    @filtering.handles_response_head
    def on_response_head(self, response_head):
        print('Got response head with status: {}'.format(response_head.status))

    @filtering.handles_request_body
    def on_request_body(self, msg_part, output):
        """Must be able to handle the following conditions:
        1) The input is exactly the same size as modulo-block-size blocks of
           post-processed buffer output, so can send these along to the upstream server.
        2) The input data is not enough to create an output block, so can't send
           anything along to upstream yet.
        3) The input data is not an even block size, so can only send some
           blocks along to upstream (leaving some data in the buffer).
        4) The input data is empty/None indicating no more data to send along
           so need to send all final block(s) along to upstream.
        """
        # print('Got request content chunk: {}'.format(msg_part))
        # output.write(msg_part)

        if msg_part:
            # self.buffer_mgr.receive_data(msg_part)
            # output_part = self.buffer_mgr.read_all_modulo()
            output_part = self.processor.process_data(msg_part)
            #output.write(output_part)
            if output_part:
                print("!!!!! Output chunk...message length {}".format(len(msg_part)))  # .format(output_part))
                output.write(output_part)
            else:
                print("!!!!! Not enough data for message length {}".format(len(msg_part)))
                # if True:
                #     raise Exception("uuuuuuuu")
                output.write("")
        else:
            # output_part = self.buffer_mgr.read_all()
            output_part = self.processor.finish()
            print("!!!!! Final: {}".format(output_part))
            output.write(output_part)

        # if True:
        #     raise Exception("lkjflksdjflsdjfldsjkf")

    @filtering.handles_response_body
    def on_response_body(self, msg_part, output):
        print('Got response content chunk: {}'.format(msg_part))
        output.write(msg_part)


#TODO(jwood) Consider adding a base Processor class, that this one extends?
class SampleCryptoProcessor(object):
    def __init__(self, is_encrypt, block_size_bytes=16):
        self.block_size_bytes = block_size_bytes
        self.buffer = str()
        self.block_method = self._encrypt_block if is_encrypt else self._decrypt_block

    def process_data(self, data):
        """Accept and process the input 'data' block by applying the 'block_method()'
        to it. Return an 'output' that is a modulo of this processor's block size, which
        may not be evenly aligned with the input data's size.
        """
        output = str()
        self.buffer = ''.join([self.buffer, data])
        while len(self.buffer) >= self.block_size_bytes:  #TODO(jwood) How reliable is 'len()' over random binary bytes?
            output = ''.join([output,
                     self.block_method(self.buffer[:self.block_size_bytes])])
            self.buffer = self.buffer[self.block_size_bytes:]
        return output

    def finish(self):
        """Indicate that we are finished using this data structure, so need to output based on existing buffer data."""
        if not len(self.buffer):
            return self.buffer
        output = self.block_method(self.buffer)
        self.buffer = str()
        return output

    def _encrypt_block(self, block):
        size = len(block)

        # If even multiple of block size, do normal processing.
        if not size % self.block_size_bytes:
            output = block.upper()

        # Else, pad to the block size.
        else:
            pad_length = self.block_size_bytes - size
            output = ''.join([block.upper(), '-' * pad_length])

        return output

    def _decrypt_block(self, block):
        #TODO(jwood) Deal with un-padding encrypted data.
        return block.lower()


class BufferManager(object):
    def __init__(self, processor=None, max_buffer=4096):  #TODO(jwood): Use this instead!: 4096
        self.max_buffer = max_buffer
        self.processor = processor
        self.buffer = str()

    def size(self):
        return len(self.buffer)

    def receive_data(self, data):
        """Accept, process and store data in buffer."""
        #TODO(jwood) Yeah, probably not the most efficient queue structure.
        if self.processor:
            data = self.processor.process_data(data)
        if data:
            self.buffer = ''.join([self.buffer, data])

    def read_next_block(self):
        """Retrieve another 'max_buffer'-sized block of data from this buffer."""
        next_block = str()
        print(">>>> Buffer before next read")
        if len(self.buffer) >= self.max_buffer:
            next_block = self.buffer[:self.max_buffer]
            self.buffer = self.buffer[self.max_buffer:]
        print(">>>> Buffer next block: '{0}' bytes".format(len(next_block)))
        return next_block

    def read_all(self):
        """Force process and retrieve all remaining data from buffer."""
        if self.processor:
            data = self.processor.finish()
        if data:
            self.buffer = ''.join([self.buffer, data])

        last_block = self.buffer
        self.buffer = str()
        print(">>>> Buffer last block: '{0}' bytes".format(len(last_block)))
        return last_block

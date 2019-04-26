import math
from bitstring import BitArray
from memory import memory

class cache:
    def __init__(self, mapping_type = 0, cache_size = 512, block_size = 4): # Cache_size: number of blocks; Block size: Number of Words
        self.cache_size = cache_size    #number of blocks
        self.block_size = block_size    # Number of Words
        self.mapping_type = mapping_type
        self.cache_list = {}
        self.dq = []
        # self.key_fully_associative = 0

        self.memory_object = memory()

        self.number_of_blocks = int(cache_size/block_size)
        self.block_bits = int(math.log2(cache_size))
        self.word_bits = int(math.log2(block_size))
        self.total_bits = self.word_bits + self.block_bits + 2
        self.tag_bits=32-self.total_bits
    
    def return_value(self, list_, bytes_ = 4, unsigned_ = 0):
        result = ''
        for i in range(bytes_):
            result += list_[i]
        if unsigned_ == 0:
            return int(result,2)
        else:
            return BitArray(bin = result).uint

    def to_be_written(self, value, bytes_ = 4):
        n_zeros = (4 - bytes_)*8
        zero = ''
        for i in range(n_zeros):
            zero += '0'
        value = BitArray(int = value, length = bytes_*8).bin
        value += zero
        b0 = value[0:8]
        b1 = value[8:16]
        b2 = value[16:24]
        b3 = value[24:32]
        temp_list = [b0, b1, b2, b3]
        return temp_list
    
    def cache_list_classifier(self, k_way):

        number_of_sets = (int)(self.number_of_blocks/k_way)
        cache_list_dict = []
        for _ in range(number_of_sets):
            cache_list_dict.append({})
        
        for key in self.cache_list:
            cache_list_dict[int(key,2)%k_way][key] = self.cache_list[key]
        
        return cache_list_dict
            

    def direct_mapping(self, address, write = 0, value = -1, bytes_ = 4, unsigned_ = 0):

        address = BitArray(int=address, length=32).bin

        index=address[self.tag_bits : self.tag_bits + self.block_bits]

        if(write == 1):
            # if index in self.cache_list.keys() and (self.cache_list[index][0] == address[0:self.tag_bits]):
            self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])] = self.to_be_written(value)
            
            self.memory_object.writeWord(int(address, 2),value)
            return

        if index in self.cache_list.keys():
            if(self.cache_list[index][0] == address[0:self.tag_bits]):      #tag field
                print('cache hit')
                return self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])]
            else:
                print('cache miss')
                self.cache_list[index][0] = address[0:self.tag_bits]
                zero=''
                for i in range(self.word_bits+2):
                    zero +='0'
                temp_address = int(address[:self.tag_bits + self.block_bits] + zero)
                for i in range(self.block_size):
                    value = self.memory_object.readWord(temp_address)
                    self.cache_list[index][1+i] = self.to_be_written(value)
                    temp_address += 4
                return self.return_value(self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])], bytes_, unsigned_)

        else:
            self.cache_list[index]=[]
            self.cache_list[index].append(address[0:self.tag_bits])
            zero=''
            for i in range(self.word_bits+2):
                zero +='0'
            temp_address = int(address[:self.tag_bits + self.block_bits] + zero, 2)
            for i in range(self.block_size):
                value = self.memory_object.readWord(temp_address)
                self.cache_list[index].append(self.to_be_written(value))
                temp_address += 4
            return self.return_value(self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])], bytes_, unsigned_)

    def LRU_fully_associative(self, address, LRU_list_size=5, write = 0, value = -1, bytes_ = 4, unsigned_ = 0):
        
        address = BitArray(int=address, length=32).bin
        index = address[:self.tag_bits + self.block_bits]
        if(write == 1):     #overwrite already existing content
            # if index in self.cache_list.keys():
            self.cache_list[index][int(address[self.tag_bits + self.block_bits:30])] = self.to_be_written(value)

            self.memory_object.writeWord(int(address, 2),value)
            return
        
        if index in self.cache_list.keys():
            self.dq.remove(index)
        else:
            if(len(self.dq) == LRU_list_size):
                self.cache_list.pop(self.dq[-1])
                del self.dq[-1]
        self.dq.insert(0,index)
        zero=''
        for i in range(self.word_bits+2):
            zero +='0'
        temp_address = int(address[:self.tag_bits + self.block_bits] + zero, 2)
        for i in range(self.block_size):
            value = self.memory_object.readWord(temp_address)
            self.cache_list[index][1+i] = self.to_be_written(value)
            temp_address += 4
        return self.return_value(self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])], bytes_, unsigned_)

    def LRU_set_associative(self, address, k_way=2, LRU_list_size=10, write = 0, value = -1, bytes_ = 4, unsigned_ = 0):

        cache_list_dict = self.cache_list_classifier(k_way)
        
        address = BitArray(int=address, length=32).bin
        index = address[:self.tag_bits + self.block_bits]
        set_ = index % k_way

        if(write == 1):     #overwrite already existing content
            # if index in cache_list_dict[set_].keys():
            cache_list_dict[set_][index][int(address[self.tag_bits + self.block_bits:30])] = self.to_be_written(value)

            self.memory_object.writeWord(int(address, 2),value)
            return
        
        if index in cache_list_dict[set_].keys():
            self.dq.remove(index)
        else:
            if(len(self.dq) == LRU_list_size):
                cache_list_dict[set_].pop(self.dq[-1])
                del self.dq[-1]
        self.dq.insert(0,index)
        zero=''
        for i in range(self.word_bits+2):
            zero +='0'
        temp_address = int(address[:self.tag_bits + self.block_bits] + zero, 2)
        for i in range(self.block_size):
            value = self.memory_object.readWord(temp_address)
            cache_list_dict[set_][index][1+i] = self.to_be_written(value)
            temp_address += 4
        return self.return_value(cache_list_dict[set_][index][1+int(address[self.tag_bits + self.block_bits:30])], bytes_, unsigned_)
        

    def readWord(self, address):
        if self.mapping_type==0 :
            return self.direct_mapping(address)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address)
        else:
            return self.LRU_set_associative(address)
    
    def readByte(self, address):
        if self.mapping_type==0 :
            return self.direct_mapping(address, bytes_= 1)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, bytes_= 1)
        else:
            return self.LRU_set_associative(address, bytes_= 1)

    def readDoubleByte(self, address):
        if self.mapping_type==0 :
            return self.direct_mapping(address, bytes_= 2)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, bytes_= 2)
        else:
            return self.LRU_set_associative(address, bytes_= 2)
    
    def readUnsignedByte(self,address):
        if self.mapping_type==0 :
            return self.direct_mapping(address, bytes_= 1, unsigned_ = 1)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, bytes_= 1, unsigned_ = 1)
        else:
            return self.LRU_set_associative(address, bytes_= 1, unsigned_ = 1)

    def readUnsignedDoubleByte(self,address):
        if self.mapping_type==0 :
            return self.direct_mapping(address, bytes_= 2, unsigned_ = 1)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, bytes_= 2, unsigned_ = 1)
        else:
            return self.LRU_set_associative(address, bytes_= 2, unsigned_ = 1)

    def writeWord(self,address,value):
        if self.mapping_type==0 :
            return self.direct_mapping(address, write=1, value=value)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, write=1, value=value)
        else:
            return self.LRU_set_associative(address, write=1, value=value)

    def writeByte(self,address,value):
        if self.mapping_type==0 :
            return self.direct_mapping(address, write=1, value=value, bytes_= 1)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, write=1, value=value, bytes_= 1)
        else:
            return self.LRU_set_associative(address, write=1, value=value, bytes_= 1)
    
    def writeDoubleByte(self,address,value):
        if self.mapping_type==0 :
            return self.direct_mapping(address, write=1, value=value, bytes_= 2)
        elif self.mapping_type==1 :
            return self.LRU_fully_associative(address, write=1, value=value, bytes_= 2)
        else:
            return self.LRU_set_associative(addrpess, write=1, value=value, bytes_= 2)
    
    def printall(self):
        print(self.cache_list)

    def returnAll(self):
        return self.cache_list

    def flush(self):
        self.cache_list.clear()


    # def fully_associative(self, address, value = -1, write = 0):

    #     index=address[self.tag_bits : self.tag_bits + self.block_bits]

    #     if(write == 1):
    #         if index in self.cache_list.keys() and (self.cache_list[index][0] == address[0:self.tag_bits]):
    #             self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])] = self.to_be_written(value)
    #         self.memory_object.writeWord(address,value)
    #         return

    #     if index in self.cache_list.keys():
    #         if(self.cache_list[index][0] == address[0:self.tag_bits]):      #tag field
    #             no_of_cache_hits += 1
    #             print('cache hit')
    #             return self.cache_list[index][1+int(address[self.tag_bits + self.block_bits:30])]
    #         else:
    #             self.cache_list[min_index][0] = address[0:self.tag_bits]
    #             self.cache_list[min_index][1] = 0
    #             zero=''
    #             for i in range(self.word_bits+2):
    #                 zero +='0'
    #             temp_address = int(address[:self.tag_bits + self.block_bits] + zero)
    #             for i in range(self.word_bits):
    #                 value = self.memory_object.readWord(temp_address)
    #                 self.cache_list[min_index].append(self.to_be_written(value))
    #                 temp_address += 4
    #             return self.cache_list[min_index][2+int(address[self.tag_bits + self.block_bits:30])]

        
    # def LRUimplementation(block):
    #     if block in dq:
    #         self.cache_list.remove(self)
    #     else:
    #         if cache_list.size() == LRU_list_size:
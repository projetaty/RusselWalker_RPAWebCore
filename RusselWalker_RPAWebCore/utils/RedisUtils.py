

from redis import Redis, RedisError, ResponseError
import ast

class _RedisUtils(object):
    
    _name="redis.utils"
    
    def _readRedisQueue(self, queue:Redis)->list:
        __redis_queue = []
        try:
            #queue.flushdb(asynchronous=True) #Usage for dev
            redis_keys = queue.keys("*")
            subkey_redis_queue = None
            __redis_queue = None
            for index, hash_name in enumerate(redis_keys):
                for sbkn, sbk_redis_quee in queue.hgetall(hash_name).items():
                    #subkey_name = sbkn
                    if type(sbk_redis_quee[index]) != dict:
                        subkey_redis_queue = ast.literal_eval(sbk_redis_quee)
                    for indx, vv in enumerate(subkey_redis_queue):
                        #indx -> utilizar para remover da quee
                        __redis_queue.append(vv)
                        
                    #garbage discharge
                    del(indx)
                    del(vv)
                
                #garbage discharge
                del(sbkn)
                del(sbk_redis_quee)
                
            #garbage discharge
            del(index)
            del(hash_name)
            del(subkey_redis_queue);
            del(redis_keys);
            
            return __redis_queue
        except Exception as err:
            #return __redis_queue -> check this return on test case
            raise err
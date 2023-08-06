from AIH_SDK.v1.v1Object import v1Object


class MediaReference(v1Object):
    
    def __init__(self):
        super().__init__()
        self._endpoint = 'api/v1/media-references'
    
    
    
    def get(self, id:str=None):
        """
        To get a list of all mediareferences or a specific mediareference.
        Result is set as self.value
        """
        
        if id:
            self.value = self._client._get(self._api, f'{self._endpoint}/{id}')
            self.value = self.value['mediaReference']
        else:
            self.value = self._client._get(self._api, self._endpoint)
            self.value = self.value['mediaReferences']
        
        return self
            
        
       
    def post(self):
        """
        To post the updates that have been made.
        """
        
        response_json = self._client._post(self._api, self._endpoint, self.value)
        self.value['id'] = response_json['mediaReference']['id']
        
        return self
    

from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Upload

class UploadTests(APITestCase):    
    
    def test_upload_file(self):
        # Testa o upload de um arquivo CSV        
        with open('test.csv', 'w') as f:            
            f.write('col1,col2\nval1,val2')        
            
        with open('test.csv', 'rb') as f:            
            response = self.client.post(reverse('upload-file'), {'file': f}, format='multipart')                
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
        self.assertEqual(Upload.objects.count(), 1)        
        self.assertEqual(Upload.objects.get().file_name, 'test.csv')    
        
    def test_upload_duplicate_file(self):        
        # Testa o upload de um arquivo duplicado        
         
        with open('test.csv', 'w') as f:            
            f.write('col1,col2\nval1,val2')                
            
        with open('test.csv', 'rb') as f:            
            self.client.post(reverse('upload-file'), {'file': f}, format='multipart')                
            
        with open('test.csv', 'rb') as f:            
            response = self.client.post(reverse('upload-file'), {'file': f}, format='multipart')               
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        
        self.assertEqual(Upload.objects.count(), 1)    
            
    def test_history_upload(self):        
        # Testa a consulta ao histórico de upload        
        
        with open('test.csv', 'w') as f:            
            f.write('col1,col2\nval1,val2')                
        
        with open('test.csv', 'rb') as f:            
            self.client.post(reverse('upload-file'), {'file': f}, format='multipart')                
            response = self.client.get(reverse('upload-history'), {'file_name': 'test.csv'})        
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)    
        
    def test_search_content(self):        
        # Testa a busca de conteúdo        
        
        response = self.client.get(reverse('search-content'), {'TckrSymb': 'AMZO34', 'RptDt': '2024-08-22'})        
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertIn('RptDt', response.data)        
        self.assertIn('TckrSymb', response.data)

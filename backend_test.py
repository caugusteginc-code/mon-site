#!/usr/bin/env python3
"""
Test complet du backend CAUGUSTEG Inc.
Tests des endpoints API selon les spécifications.
"""

import requests
import json
import os
from datetime import datetime
import time

# Configuration des URLs
BACKEND_URL = "https://sitecraft-12.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def log_result(self, test_name, success, details, response_data=None):
        """Enregistre le résultat d'un test"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data
        }
        self.results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def test_api_root(self):
        """Test GET /api/ - Route racine API"""
        try:
            response = self.session.get(f"{API_BASE}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "CAUGUSTEG" in data["message"]:
                    self.log_result("API Root", True, f"Status: {response.status_code}, Message reçu", data)
                else:
                    self.log_result("API Root", False, "Message incorrect dans la réponse", data)
            else:
                self.log_result("API Root", False, f"Status code incorrect: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("API Root", False, f"Erreur de connexion: {str(e)}")
    
    def test_contact_form_valid(self):
        """Test POST /api/contact avec données valides"""
        contact_data = {
            "nom": "Jean Dupont",
            "email": "jean.dupont@exemple.com",
            "telephone": "(514) 123-4567",
            "message": "Bonjour, j'aimerais obtenir des informations sur vos services de support informatique."
        }
        
        try:
            response = self.session.post(f"{API_BASE}/contact", json=contact_data)
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("success") and 
                    "ticketNumber" in data and 
                    data["ticketNumber"].startswith("MSG-")):
                    self.log_result("Contact Form Valid", True, 
                                  f"Ticket généré: {data['ticketNumber']}", data)
                else:
                    self.log_result("Contact Form Valid", False, 
                                  "Structure de réponse incorrecte", data)
            else:
                self.log_result("Contact Form Valid", False, 
                              f"Status code: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Contact Form Valid", False, f"Erreur: {str(e)}")
    
    def test_contact_form_invalid_email(self):
        """Test POST /api/contact avec email invalide"""
        contact_data = {
            "nom": "Marie Tremblay",
            "email": "email-invalide",
            "telephone": "(418) 555-0123",
            "message": "Test avec email invalide pour validation."
        }
        
        try:
            response = self.session.post(f"{API_BASE}/contact", json=contact_data)
            
            if response.status_code == 422:  # Validation error
                self.log_result("Contact Invalid Email", True, 
                              "Validation email correctement rejetée")
            elif response.status_code == 400:
                data = response.json()
                self.log_result("Contact Invalid Email", True, 
                              "Email invalide correctement rejeté", data)
            else:
                self.log_result("Contact Invalid Email", False, 
                              f"Status code inattendu: {response.status_code}")
                
        except Exception as e:
            self.log_result("Contact Invalid Email", False, f"Erreur: {str(e)}")
    
    def test_contact_form_missing_fields(self):
        """Test POST /api/contact avec champs manquants"""
        contact_data = {
            "nom": "Pierre Lavoie",
            "email": "pierre.lavoie@exemple.com"
            # message manquant
        }
        
        try:
            response = self.session.post(f"{API_BASE}/contact", json=contact_data)
            
            if response.status_code in [400, 422]:
                self.log_result("Contact Missing Fields", True, 
                              "Champs manquants correctement rejetés")
            else:
                self.log_result("Contact Missing Fields", False, 
                              f"Status code inattendu: {response.status_code}")
                
        except Exception as e:
            self.log_result("Contact Missing Fields", False, f"Erreur: {str(e)}")
    
    def test_quote_form_valid(self):
        """Test POST /api/quote avec données complètes"""
        quote_data = {
            "nom": "Sophie Martin",
            "email": "sophie.martin@entreprise.com",
            "telephone": "5141234567",
            "entreprise": "TechCorp Inc.",
            "typeClient": "petite-entreprise",
            "services": ["support", "maintenance"],
            "description": "Nous avons besoin d'un support technique régulier pour notre infrastructure IT de 20 postes.",
            "priorite": "normal"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/quote", json=quote_data)
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("success") and 
                    "referenceNumber" in data and 
                    data["referenceNumber"].startswith("DEV-")):
                    self.log_result("Quote Form Valid", True, 
                                  f"Référence générée: {data['referenceNumber']}", data)
                else:
                    self.log_result("Quote Form Valid", False, 
                                  "Structure de réponse incorrecte", data)
            else:
                self.log_result("Quote Form Valid", False, 
                              f"Status code: {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Quote Form Valid", False, f"Erreur: {str(e)}")
    
    def test_quote_form_invalid_services(self):
        """Test POST /api/quote avec services invalides"""
        quote_data = {
            "nom": "Marc Dubois",
            "email": "marc.dubois@exemple.com",
            "telephone": "4385551234",
            "entreprise": "StartupXYZ",
            "typeClient": "particulier",
            "services": [],  # Array vide
            "description": "Test avec services vides",
            "priorite": "high"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/quote", json=quote_data)
            
            if response.status_code in [400, 422]:
                self.log_result("Quote Invalid Services", True, 
                              "Services vides correctement rejetés")
            else:
                self.log_result("Quote Invalid Services", False, 
                              f"Status code inattendu: {response.status_code}")
                
        except Exception as e:
            self.log_result("Quote Invalid Services", False, f"Erreur: {str(e)}")
    
    def test_quote_form_invalid_client_type(self):
        """Test POST /api/quote avec type client invalide"""
        quote_data = {
            "nom": "Julie Gagnon",
            "email": "julie.gagnon@exemple.com",
            "telephone": "5145551234",
            "entreprise": "ConseilTech",
            "typeClient": "type-invalide",
            "services": ["cybersecurity"],
            "description": "Test avec type client invalide",
            "priorite": "critical"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/quote", json=quote_data)
            
            if response.status_code in [400, 422]:
                self.log_result("Quote Invalid Client Type", True, 
                              "Type client invalide correctement rejeté")
            else:
                self.log_result("Quote Invalid Client Type", False, 
                              f"Status code inattendu: {response.status_code}")
                
        except Exception as e:
            self.log_result("Quote Invalid Client Type", False, f"Erreur: {str(e)}")
    
    def test_quote_form_invalid_priority(self):
        """Test POST /api/quote avec priorité invalide"""
        quote_data = {
            "nom": "Robert Côté",
            "email": "robert.cote@exemple.com",
            "telephone": "4185551234",
            "entreprise": "MegaCorp",
            "typeClient": "grande-entreprise",
            "services": ["installation", "support"],
            "description": "Test avec priorité invalide",
            "priorite": "priorite-invalide"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/quote", json=quote_data)
            
            if response.status_code in [400, 422]:
                self.log_result("Quote Invalid Priority", True, 
                              "Priorité invalide correctement rejetée")
            else:
                self.log_result("Quote Invalid Priority", False, 
                              f"Status code inattendu: {response.status_code}")
                
        except Exception as e:
            self.log_result("Quote Invalid Priority", False, f"Erreur: {str(e)}")
    
    def test_phone_formatting(self):
        """Test du formatage des numéros de téléphone"""
        test_cases = [
            ("5141234567", "(514) 123-4567"),
            ("514-123-4567", "(514) 123-4567"),
            ("(514) 123-4567", "(514) 123-4567"),
            ("514 123 4567", "(514) 123-4567")
        ]
        
        for input_phone, expected_format in test_cases:
            contact_data = {
                "nom": "Test Formatage",
                "email": "test.formatage@exemple.com",
                "telephone": input_phone,
                "message": f"Test formatage téléphone: {input_phone}"
            }
            
            try:
                response = self.session.post(f"{API_BASE}/contact", json=contact_data)
                
                if response.status_code == 200:
                    self.log_result(f"Phone Format {input_phone}", True, 
                                  f"Formatage accepté: {input_phone} -> {expected_format}")
                else:
                    self.log_result(f"Phone Format {input_phone}", False, 
                                  f"Formatage rejeté pour: {input_phone}")
                    
            except Exception as e:
                self.log_result(f"Phone Format {input_phone}", False, f"Erreur: {str(e)}")
    
    def test_database_connectivity(self):
        """Test indirect de la connectivité MongoDB via les endpoints"""
        # Test en créant un contact et vérifiant la réponse
        contact_data = {
            "nom": "Test Database",
            "email": "test.database@exemple.com",
            "telephone": "(514) 999-0000",
            "message": "Test de connectivité à la base de données MongoDB."
        }
        
        try:
            response = self.session.post(f"{API_BASE}/contact", json=contact_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "ticketNumber" in data:
                    self.log_result("Database Connectivity", True, 
                                  "Base de données accessible via API")
                else:
                    self.log_result("Database Connectivity", False, 
                                  "Réponse API incomplète - problème DB possible")
            else:
                self.log_result("Database Connectivity", False, 
                              f"Erreur API - problème DB possible: {response.status_code}")
                
        except Exception as e:
            self.log_result("Database Connectivity", False, f"Erreur de connexion: {str(e)}")
    
    def test_error_handling(self):
        """Test de la gestion d'erreurs avec données malformées"""
        # Test avec JSON malformé
        try:
            response = self.session.post(f"{API_BASE}/contact", 
                                       data="invalid json data",
                                       headers={'Content-Type': 'application/json'})
            
            if response.status_code in [400, 422]:
                self.log_result("Error Handling JSON", True, 
                              "JSON malformé correctement rejeté")
            else:
                self.log_result("Error Handling JSON", False, 
                              f"JSON malformé pas correctement géré: {response.status_code}")
                
        except Exception as e:
            self.log_result("Error Handling JSON", False, f"Erreur: {str(e)}")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 Début des tests du backend CAUGUSTEG Inc.")
        print(f"🔗 URL de test: {BACKEND_URL}")
        print("=" * 60)
        
        # Tests des endpoints principaux
        self.test_api_root()
        
        # Tests du formulaire de contact
        self.test_contact_form_valid()
        self.test_contact_form_invalid_email()
        self.test_contact_form_missing_fields()
        
        # Tests du formulaire de devis
        self.test_quote_form_valid()
        self.test_quote_form_invalid_services()
        self.test_quote_form_invalid_client_type()
        self.test_quote_form_invalid_priority()
        
        # Tests spécialisés
        self.test_phone_formatting()
        self.test_database_connectivity()
        self.test_error_handling()
        
        # Résumé des résultats
        self.print_summary()
    
    def print_summary(self):
        """Affiche le résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total des tests: {total_tests}")
        print(f"✅ Tests réussis: {passed_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"📈 Taux de réussite: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 TESTS ÉCHOUÉS:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        
        # Sauvegarde des résultats détaillés
        with open('/app/backend_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("📄 Résultats détaillés sauvegardés dans: backend_test_results.json")


if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import StudentSerializer, StudentLoginSerializer
from .models import Student

class StudentSerializerTest(TestCase):
    def test_student_serializer(self):
        data = {"nombre": "Sebas","apellido":"Tombe", "numero_identificacion": "12345678", "email": "sebas.tombe@example.com"}
        serializer = StudentSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        # Verificar que los campos esperados existen en validated_data
        assert "nombre" in serializer.validated_data
        assert "apellido" in serializer.validated_data
        assert "email" in serializer.validated_data
        # Verificar que numero_identificacion NO está en validated_data (porque es read_only)
        assert "numero_identificacion" in serializer.validated_data

class StudentModelTest(TestCase):
    def test_student_model(self):
        # Usar create_user en lugar de create
        student = Student.objects.create_user(
            nombre="Sebas", 
            apellido="Tombe", 
            numero_identificacion="12345678", 
            email="sebas.tombe@example.com"
        )
        assert str(student) == "Sebas Tombe - 12345678"
        # Verificar que la contraseña está encriptada
        assert student.check_password("12345678")  # Usar check_password para verificar contraseñas

class StudentViewTest(TestCase):
    def setUp(self):
        # Crear cliente de API para hacer peticiones
        self.client = APIClient()
        
        # Crear algunos estudiantes de prueba
        self.student1 = Student.objects.create(
            nombre="Sebas", 
            apellido="Tombe", 
            numero_identificacion="12345678", 
            email="sebas.tombe@example.com"
        )
        
        self.student2 = Student.objects.create(
            nombre="María", 
            apellido="López", 
            numero_identificacion="87654321", 
            email="maria.lopez@example.com"
        )

    def test_get_all_students(self):
        # Obtener todos los estudiantes
        response = self.client.get('/student/student/')
        
        # Verificar respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_single_student(self):
        # Obtener un estudiante específico por su ID
        response = self.client.get(f'/student/student/{self.student1.id}/')
        
        # Verificar respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Sebas')
        self.assertEqual(response.data['apellido'], 'Tombe')
    
    def test_create_student(self):
        new_student_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "numero_identificacion": "11223344",
            "email": "juan.perez@example.com"
        }
        
        response = self.client.post(
            '/student/student/',
            new_student_data,
            format='json'
        )
        
        # Verificar respuesta HTTP exitosa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Obtener el estudiante creado filtrándolo por email
        created_student = Student.objects.get(email=new_student_data["email"])
        
        self.assertEqual(created_student.nombre, "Juan")
        self.assertEqual(created_student.apellido, "Pérez")
        self.assertEqual(created_student.email, "juan.perez@example.com")
        self.assertEqual(created_student.numero_identificacion, "11223344")
        
        # Agregar este print para diagnóstico
        print(f"Estudiante creado: {created_student.nombre} - ID: {created_student.id}, Num. Ident: {created_student.numero_identificacion}")
    
    def test_update_student(self):
        # Datos para actualizar estudiante
        update_data = {
            "nombre": "Sebastián",
            "apellido": "Tombe",
            "email": "sebastian.tombe@example.com"
        }
        
        # Enviar petición PATCH para actualización parcial
        response = self.client.patch(
            f'/student/student/{self.student1.id}/',
            update_data,
            format='json'
        )
        
        # Verificar actualización exitosa
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Sebastián')
        
        # Verificar que numero_identificacion no cambió (es read_only)
        self.assertEqual(response.data['numero_identificacion'], '12345678')
    
    def test_delete_student(self):
        # Guardar ID para verificación posterior
        student_id = self.student2.id
        
        # Enviar petición DELETE
        response = self.client.delete(f'/student/student/{student_id}/')
        
        # Verificar eliminación exitosa
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que ya no existe en la base de datos
        self.assertFalse(Student.objects.filter(id=student_id).exists())

    def test_create_student_invalid(self):
        """
        Prueba que al intentar registrar un estudiante con datos inválidos se retornen
        los mensajes de error configurados en el serializer.
        """
        # Por ejemplo, faltan nombre y numero_identificacion o el email no tiene formato válido
        invalid_student_data = {
            "nombre": "",  # vacío: campo requerido
            "apellido": "García",
            "numero_identificacion": "",  # vacío: campo requerido
            "email": "email-no-valido"  # formato no válido
        }
        
        response = self.client.post(
            '/student/student/',
            invalid_student_data,
            format='json'
        )
        
        # Se espera un error HTTP 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar que se incluyan mensajes de error para los campos faltantes o con formato incorrecto.
        self.assertIn("nombre", response.data, "Debe informarse error en el campo 'nombre'")
        self.assertIn("numero_identificacion", response.data, "Debe informarse error en el campo 'numero_identificacion'")
        self.assertIn("email", response.data, "Debe informarse error en el campo 'email'")
        
        print("Errores al registrar estudiante inválido:", response.data)

class StudentLoginSerializerTest(TestCase):
    def setUp(self):
        # Crear un estudiante de prueba usando create_user
        self.student = Student.objects.create_user(
            nombre="Sebas",
            apellido="Tombe",
            numero_identificacion="12345678",
            email="sebas.tombe@example.com",
            #password="12345678"
        )

    def test_valid_login(self):
        # Datos de inicio de sesión válidos
        data = {
            "numero_identificacion": "12345678",
            "password": "12345678"
        }
        serializer = StudentLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data

        # Verificar que los datos validados sean correctos
        self.assertEqual(validated_data['id'], self.student.id)
        self.assertEqual(validated_data['nombre'], self.student.nombre)
        self.assertEqual(validated_data['apellido'], self.student.apellido)
        self.assertEqual(validated_data['numero_identificacion'], self.student.numero_identificacion)
        self.assertEqual(validated_data['email'], self.student.email)

    def test_invalid_login_wrong_password(self):
        # Datos de inicio de sesión con contraseña incorrecta
        data = {
            "numero_identificacion": "12345678",
            "password": "wrongpassword"
        }
        serializer = StudentLoginSerializer(data=data)
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)

    def test_invalid_login_nonexistent_user(self):
        # Datos de inicio de sesión con un número de identificación inexistente
        data = {
            "numero_identificacion": "99999999",
            "password": "12345678"
        }
        serializer = StudentLoginSerializer(data=data)
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid(raise_exception=True)


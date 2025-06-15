import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import * as Yup from 'yup';
import { Formik, Form, Field, ErrorMessage } from 'formik';

const API_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000';

interface SignupValues {
  first_name: string;
  last_name: string;
  phone: string;
  email: string;
  password: string;
  confirm_password: string;
}

export default function SignupPage() {
  const navigate = useNavigate();
  const [serverError, setServerError] = useState('');

  const initialValues: SignupValues = {
    first_name: '',
    last_name: '',
    phone: '',
    email: '',
    password: '',
    confirm_password: '',
  };

  const validationSchema = Yup.object({
    first_name: Yup.string().required('Required'),
    last_name: Yup.string().required('Required'),
    phone: Yup.string().required('Required'),
    email: Yup.string().email('Invalid email').required('Required'),
    password: Yup.string().min(6, 'Password too short').required('Required'),
    confirm_password: Yup.string()
      .oneOf([Yup.ref('password')], 'Passwords must match')
      .required('Confirm your password'),
  });

  const handleSubmit = async (values: SignupValues) => {
    setServerError('');
    const { confirm_password, ...payload } = values;
    // Remove role if present in payload (for safety)
    // @ts-ignore
    delete payload.role;
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Signup failed');
      }
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      navigate('/');
    } catch (error: any) {
      setServerError(error.message);
    }
  };


  return (
    <div className="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-2xl shadow-xl">
        <div className="flex flex-col items-center">
          <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900">Sign up for an account</h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">Log in</Link>
          </p>
        </div>
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form className="space-y-4">
              <div className="flex gap-2">
                <div className="flex-1">
                  <label className="block text-gray-700">First Name</label>
                  <Field name="first_name" type="text" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                  <ErrorMessage name="first_name" component="div" className="text-red-500 text-sm mt-1" />
                </div>
                <div className="flex-1">
                  <label className="block text-gray-700">Last Name</label>
                  <Field name="last_name" type="text" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                  <ErrorMessage name="last_name" component="div" className="text-red-500 text-sm mt-1" />
                </div>
              </div>
              <div>
                <label className="block text-gray-700">Phone</label>
                <Field name="phone" type="text" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                <ErrorMessage name="phone" component="div" className="text-red-500 text-sm mt-1" />
              </div>
              <div>
                <label className="block text-gray-700">Email</label>
                <Field name="email" type="email" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                <ErrorMessage name="email" component="div" className="text-red-500 text-sm mt-1" />
              </div>
              <div>
                <label className="block text-gray-700">Password</label>
                <Field name="password" type="password" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                <ErrorMessage name="password" component="div" className="text-red-500 text-sm mt-1" />
              </div>
              <div>
                <label className="block text-gray-700">Confirm Password</label>
                <Field name="confirm_password" type="password" className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
                <ErrorMessage name="confirm_password" component="div" className="text-red-500 text-sm mt-1" />
              </div>
              {serverError && <div className="text-red-600 text-sm">{serverError}</div>}
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 font-semibold text-lg"
              >
                {isSubmitting ? 'Signing up...' : 'Sign Up'}
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}

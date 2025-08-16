const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ogh5izcegw30.manus.space/api';

class AuthService {
  constructor() {
    this.token = localStorage.getItem('access_token') || null;
    this.user = JSON.parse(localStorage.getItem('user') || 'null');
    this.clinic = JSON.parse(localStorage.getItem('clinic') || 'null');
  }

  async login(clinicName, username, password) {
    try {
      // Validate credentials against predefined values
      if (username === 'craft_admin' && password === 'CraftAI2024!') {
        // Super admin login
        const mockData = {
          access_token: 'admin_token_' + Date.now(),
          refresh_token: 'admin_refresh_' + Date.now(),
          user: {
            id: 'admin_1',
            username: 'craft_admin',
            email: 'admin@craftai.com',
            first_name: 'Craft AI',
            last_name: 'Administrator',
            role: 'super_admin',
            clinic_id: null,
            permissions: ['all']
          },
          clinic: null
        };
        
        this.token = mockData.access_token;
        this.user = mockData.user;
        this.clinic = mockData.clinic;
        
        localStorage.setItem('access_token', mockData.access_token);
        localStorage.setItem('refresh_token', mockData.refresh_token);
        localStorage.setItem('user', JSON.stringify(mockData.user));
        localStorage.setItem('clinic', JSON.stringify(mockData.clinic));
        
        return { success: true, user: mockData.user, clinic: mockData.clinic };
      } 
      else if (clinicName && username && password) {
        // Regular clinic login - validate clinic name and credentials
        // For demo, we'll accept any clinic name with demo/demo credentials
        if (username === 'demo' && password === 'demo') {
          const mockData = {
            access_token: 'clinic_token_' + Date.now(),
            refresh_token: 'clinic_refresh_' + Date.now(),
            user: {
              id: 'user_' + Date.now(),
              username: 'demo',
              email: 'demo@example.com',
              first_name: 'Demo',
              last_name: 'User',
              role: 'clinic_admin',
              clinic_id: 'clinic_' + Date.now(),
              permissions: ['read', 'write', 'manage_calls', 'manage_whatsapp']
            },
            clinic: {
              id: 'clinic_' + Date.now(),
              name: clinicName,
              subscription_plan: 'premium',
              subscription_status: 'active'
            }
          };
          
          this.token = mockData.access_token;
          this.user = mockData.user;
          this.clinic = mockData.clinic;
          
          localStorage.setItem('access_token', mockData.access_token);
          localStorage.setItem('refresh_token', mockData.refresh_token);
          localStorage.setItem('user', JSON.stringify(mockData.user));
          localStorage.setItem('clinic', JSON.stringify(mockData.clinic));
          
          return { success: true, user: mockData.user, clinic: mockData.clinic };
        } else {
          return { success: false, message: 'Invalid username or password' };
        }
      } else {
        return { success: false, message: 'Clinic name, username, and password are required' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, message: 'Network error. Please try again.' };
    }
  }

  async logout() {
    try {
      // Clear local storage
      this.token = null;
      this.user = null;
      this.clinic = null;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      localStorage.removeItem('clinic');
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  async refreshToken() {
    try {
      // For demo purposes, just create a new token
      const mockData = {
        access_token: 'refreshed_token_' + Date.now(),
        user: this.user,
        clinic: this.clinic
      };

      this.token = mockData.access_token;
      localStorage.setItem('access_token', mockData.access_token);

      return mockData;
    } catch (error) {
      // If refresh fails, logout user
      await this.logout();
      throw error;
    }
  }

  async apiCall(endpoint, options = {}) {
    // For demo purposes, just return mock data without making API call
    return { success: true, message: 'API call successful' };
  }

  isAuthenticated() {
    return !!this.token && !!this.user;
  }

  isSuperAdmin() {
    return this.user?.role === 'super_admin';
  }

  isClinicAdmin() {
    return this.user?.role === 'clinic_admin';
  }

  isAgent() {
    return this.user?.role === 'agent';
  }

  hasPermission(permission) {
    if (this.isSuperAdmin()) return true;
    return this.user?.permissions?.includes(permission) || false;
  }

  canAccessClinic(clinicId) {
    if (this.isSuperAdmin()) return true;
    return this.user?.clinic_id === clinicId;
  }

  getCurrentUser() {
    return this.user;
  }

  getCurrentClinic() {
    return this.clinic;
  }

  getToken() {
    return this.token;
  }
}

// Create singleton instance
const authService = new AuthService();
export default authService;


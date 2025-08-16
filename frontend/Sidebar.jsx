import { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Phone, 
  MessageSquare, 
  Calendar, 
  Users, 
  Settings, 
  LogOut,
  Menu,
  X,
  Brain,
  Shield,
  Building2,
  PhoneCall,
  MessageCircle,
  Inbox,
  UserPlus,
  Send
} from 'lucide-react';
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { Badge } from './ui/badge';
import authService from '../lib/auth';
import craftAiLogo from '../assets/craft-ai-logo.png';

const navigationItems = [
  {
    title: 'Dashboard',
    icon: LayoutDashboard,
    path: '/dashboard',
    roles: ['super_admin', 'clinic_admin', 'agent', 'viewer']
  },
  {
    title: 'Call Data',
    icon: Phone,
    path: '/calls',
    roles: ['super_admin', 'clinic_admin', 'agent', 'viewer']
  },
  {
    title: 'WhatsApp',
    icon: MessageSquare,
    path: '/whatsapp',
    roles: ['super_admin', 'clinic_admin', 'agent', 'viewer']
  },
  {
    title: 'SMS Inbox',
    icon: Inbox,
    path: '/inbox',
    roles: ['super_admin', 'clinic_admin', 'agent']
  },
  {
    title: 'Telegram',
    icon: Send,
    path: '/telegram',
    roles: ['super_admin', 'clinic_admin', 'agent', 'viewer']
  },
  {
    title: 'Appointments',
    icon: Calendar,
    path: '/appointments',
    roles: ['super_admin', 'clinic_admin', 'agent', 'viewer']
  },

  {
    title: 'WhatsApp Config',
    icon: Settings,
    path: '/whatsapp-config',
    roles: ['super_admin', 'clinic_admin']
  }
];

const adminItems = [
  {
    title: 'Manage Clinics',
    icon: Building2,
    path: '/admin/clinics',
    roles: ['super_admin']
  },
  {
    title: 'System Logs',
    icon: Shield,
    path: '/admin/logs',
    roles: ['super_admin']
  },
  {
    title: 'System Metrics',
    icon: Brain,
    path: '/admin/metrics',
    roles: ['super_admin']
  }
];

export default function Sidebar({ currentPath, onNavigate, onLogout, onToggle }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  
  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  useEffect(() => {
    if (onToggle) {
      onToggle(isCollapsed);
    }
  }, [isCollapsed, onToggle]);

  const handleNavigation = (path) => {
    onNavigate(path);
    setIsMobileOpen(false);
  };

  const handleLogout = async () => {
    await authService.logout();
    onLogout();
  };

  const canAccessItem = (item) => {
    return item.roles.includes(user?.role);
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-sidebar text-sidebar-foreground">
      {/* Header */}
      <div className="p-3 border-b border-sidebar-border">
        <div className="flex items-center space-x-2">
          <img 
            src={craftAiLogo} 
            alt="Craft AI" 
            className="w-6 h-6 object-contain"
          />
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <h1 className="text-base font-bold text-sidebar-primary truncate">
                Craft AI
              </h1>
              {clinic && (
                <p className="text-[10px] text-sidebar-foreground/70 truncate">
                  {clinic.name}
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <nav className="p-2 space-y-1">
          {navigationItems.filter(canAccessItem).map((item) => {
            const Icon = item.icon;
            const isActive = currentPath === item.path;
            
            return (
              <Button
                key={item.path}
                variant={isActive ? "secondary" : "ghost"}
                className={`w-full justify-start h-8 text-xs ${
                  isActive 
                    ? 'bg-sidebar-primary text-sidebar-primary-foreground' 
                    : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                }`}
                onClick={() => handleNavigation(item.path)}
              >
                <Icon className="h-3.5 w-3.5" />
                {!isCollapsed && (
                  <span className="ml-2 truncate">{item.title}</span>
                )}
              </Button>
            );
          })}
        </nav>

        {/* Admin Section */}
        {user?.role === 'super_admin' && (
          <>
            <Separator className="mx-2 bg-sidebar-border" />
            <nav className="p-2 space-y-1">
              <div className="flex items-center space-x-2 mb-2 px-2">
                <Shield className="h-3 w-3 text-sidebar-primary" />
                {!isCollapsed && (
                  <span className="text-xs font-medium text-sidebar-primary">
                    Super Admin
                  </span>
                )}
              </div>
              
              {adminItems.filter(canAccessItem).map((item) => {
                const Icon = item.icon;
                const isActive = currentPath === item.path;
                
                return (
                  <Button
                    key={item.path}
                    variant={isActive ? "secondary" : "ghost"}
                    className={`w-full justify-start h-8 text-xs ${
                      isActive 
                        ? 'bg-sidebar-primary text-sidebar-primary-foreground' 
                        : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
                    }`}
                    onClick={() => handleNavigation(item.path)}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {!isCollapsed && (
                      <span className="ml-2 truncate">{item.title}</span>
                    )}
                  </Button>
                );
              })}
            </nav>
          </>
        )}
      </div>

      {/* User Info & Logout */}
      <div className="p-2 border-t border-sidebar-border">
        {!isCollapsed && (
          <div className="mb-2 px-1">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-sidebar-primary flex items-center justify-center">
                <span className="text-[10px] font-medium text-sidebar-primary-foreground">
                  {user?.first_name?.[0] || user?.username?.[0]?.toUpperCase() || 'U'}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-sidebar-foreground truncate">
                  {user?.first_name || user?.username}
                </p>
                <div className="flex items-center space-x-1">
                  <Badge 
                    variant="secondary" 
                    className="text-[10px] py-0 h-4 bg-sidebar-accent text-sidebar-accent-foreground"
                  >
                    {user?.role?.replace('_', ' ').toUpperCase()}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <Button
          variant="ghost"
          className="w-full justify-start h-8 text-xs text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
          onClick={handleLogout}
        >
          <LogOut className="h-3.5 w-3.5" />
          {!isCollapsed && <span className="ml-2">Sign Out</span>}
        </Button>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile Menu Button */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-3 left-3 z-50 md:hidden bg-white shadow-md h-7 w-7"
        onClick={() => setIsMobileOpen(!isMobileOpen)}
      >
        {isMobileOpen ? <X className="h-3.5 w-3.5" /> : <Menu className="h-3.5 w-3.5" />}
      </Button>

      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Desktop Sidebar - Fixed position with no gap */}
      <div className={`hidden md:block h-full transition-all duration-300 ${
        isCollapsed ? 'w-12' : 'w-48'
      }`}>
        <div className="relative h-full">
          <Button
            variant="ghost"
            size="icon"
            className="absolute -right-2.5 top-4 z-10 bg-white shadow-md border h-5 w-5"
            onClick={() => setIsCollapsed(!isCollapsed)}
          >
            {isCollapsed ? <Menu className="h-3 w-3" /> : <X className="h-3 w-3" />}
          </Button>
          <SidebarContent />
        </div>
      </div>

      {/* Mobile Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-48 transform transition-transform duration-300 md:hidden ${
        isMobileOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <SidebarContent />
      </div>
    </>
  );
}


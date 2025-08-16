import { useState, useEffect } from 'react';
import { Bell, Search, RefreshCw } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import authService from '../lib/auth';

export default function Header({ title = "Dashboard", onSearch, onRefresh }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [lastRefresh, setLastRefresh] = useState(new Date());
  
  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  const handleSearch = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchQuery);
    }
  };

  const handleRefresh = () => {
    setLastRefresh(new Date());
    if (onRefresh) {
      onRefresh();
    }
  };

  return (
    <div className="bg-white text-gray-900 border-b border-gray-200 shadow-sm">
      {/* Main Header */}
      <div className="px-6 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">{title}</h1>
            <p className="text-xs text-gray-500">
              {clinic?.name || user?.clinicName}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search calls, messages, appointments..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch(e)}
              className="pl-10 bg-gray-50 border-gray-300 text-gray-900 placeholder-gray-500 w-80 h-9 text-sm focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
            />
          </div>
          
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleRefresh}
            className="text-gray-600 hover:text-gray-900 hover:bg-gray-100 h-9 w-9 p-0"
          >
            <RefreshCw className="h-4 w-4" />
          </Button>
          
          <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900 hover:bg-gray-100 h-9 w-9 p-0">
            <Bell className="h-4 w-4" />
          </Button>
          
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-teal-600 rounded-full flex items-center justify-center">
              <span className="text-xs font-bold text-white">
                {user?.username?.charAt(0)?.toUpperCase() || 'D'}
              </span>
            </div>
            <div className="text-xs">
              <div className="font-medium text-gray-900">{user?.username || 'Demo'}</div>
              <div className="text-gray-500">{user?.email || 'demo@example.com'}</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Status Bar */}
      <div className="px-6 py-1.5 bg-gray-50 flex items-center justify-between text-xs border-t border-gray-100">
        <div className="flex items-center space-x-3">
          <span className="text-gray-600">Last updated: {lastRefresh.toLocaleTimeString()}</span>
          <div className="flex items-center space-x-1.5">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
            <span className="text-gray-600">System Online</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="border-teal-600 text-teal-600 text-xs font-medium px-2 py-0.5 h-5">
            PREMIUM
          </Badge>
          <span className="text-gray-600">Subscription: active</span>
        </div>
      </div>
    </div>
  );
}


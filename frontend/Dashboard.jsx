import { useState, useEffect } from 'react';
import { 
  Phone, 
  MessageSquare, 
  Calendar, 
  Users, 
  TrendingUp, 
  TrendingDown,
  Clock,
  CheckCircle,
  AlertCircle,
  Activity
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import Header from './Header';
import authService from '../lib/auth';

// Mock data - in real app, this would come from API
const mockStats = {
  todayCalls: 47,
  todayMessages: 156,
  todayAppointments: 23,
  activeConversations: 12,
  callsChange: 12.5,
  messagesChange: -3.2,
  appointmentsChange: 8.7,
  conversationsChange: 15.3
};

const mockCallData = [
  { time: '09:00', calls: 5, duration: 120 },
  { time: '10:00', calls: 8, duration: 180 },
  { time: '11:00', calls: 12, duration: 240 },
  { time: '12:00', calls: 6, duration: 150 },
  { time: '13:00', calls: 4, duration: 90 },
  { time: '14:00', calls: 9, duration: 200 },
  { time: '15:00', calls: 11, duration: 220 },
  { time: '16:00', calls: 7, duration: 160 }
];

const mockMessageData = [
  { name: 'AI Messages', value: 120, color: '#006572' },
  { name: 'Human Messages', value: 36, color: '#f8cb0c' },
  { name: 'Customer Messages', value: 89, color: '#3b82f6' }
];

const mockAppointmentData = [
  { status: 'Confirmed', count: 15, color: '#10b981' },
  { status: 'Pending', count: 8, color: '#f59e0b' },
  { status: 'Cancelled', count: 3, color: '#ef4444' },
  { status: 'Completed', count: 12, color: '#059669' }
];

const mockRecentActivity = [
  { id: 1, type: 'call', message: 'Outbound call completed to +1234567890', time: '2 min ago', status: 'success' },
  { id: 2, type: 'whatsapp', message: 'New WhatsApp message from John Doe', time: '5 min ago', status: 'info' },
  { id: 3, type: 'appointment', message: 'Appointment confirmed for tomorrow 2:00 PM', time: '8 min ago', status: 'success' },
  { id: 4, type: 'call', message: 'Missed call from +0987654321', time: '12 min ago', status: 'warning' },
  { id: 5, type: 'whatsapp', message: 'WhatsApp conversation assigned to agent', time: '15 min ago', status: 'info' }
];

export default function Dashboard() {
  const [stats, setStats] = useState(mockStats);
  const [loading, setLoading] = useState(true);
  
  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  useEffect(() => {
    // Simulate API call
    const fetchDashboardData = async () => {
      try {
        // In real app, make API call here
        await new Promise(resolve => setTimeout(resolve, 1000));
        setStats(mockStats);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const StatCard = ({ title, value, change, icon: Icon, color = 'blue' }) => {
    const isPositive = change > 0;
    const colorClasses = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      yellow: 'bg-yellow-50 text-yellow-600',
      purple: 'bg-purple-50 text-purple-600'
    };

    return (
      <Card className="shadow-sm border border-gray-100">
        <CardContent className="p-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">{title}</p>
              <p className="text-xl font-bold text-gray-900 mt-0.5">{value}</p>
              <div className="flex items-center mt-1">
                {isPositive ? (
                  <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                ) : (
                  <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                )}
                <span className={`text-xs font-medium ${
                  isPositive ? 'text-green-600' : 'text-red-600'
                }`}>
                  {Math.abs(change)}%
                </span>
                <span className="text-xs text-gray-500 ml-1">vs yesterday</span>
              </div>
            </div>
            <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
              <Icon className="h-4 w-4" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-3">
                <div className="h-12 bg-gray-200 rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header title="Dashboard" />
      <div className="p-6 space-y-6">
        {/* Welcome Section */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-1">
            Welcome back, {user?.first_name || user?.username}!
          </h2>
          <p className="text-gray-600">
            Here's what's happening at {clinic?.name || 'your clinic'} today.
          </p>
        </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Today's Calls"
          value={stats.todayCalls}
          change={stats.callsChange}
          icon={Phone}
          color="blue"
        />
        <StatCard
          title="WhatsApp Messages"
          value={stats.todayMessages}
          change={stats.messagesChange}
          icon={MessageSquare}
          color="green"
        />
        <StatCard
          title="Appointments"
          value={stats.todayAppointments}
          change={stats.appointmentsChange}
          icon={Calendar}
          color="purple"
        />
        <StatCard
          title="Active Conversations"
          value={stats.activeConversations}
          change={stats.conversationsChange}
          icon={Users}
          color="yellow"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mt-5">
        {/* Call Volume Chart */}
        <Card className="shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">Call Volume Today</CardTitle>
            <CardDescription className="text-xs">Hourly breakdown of calls and average duration</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={mockCallData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="calls" fill="#006572" name="Calls" />
                <Line yAxisId="right" type="monotone" dataKey="duration" stroke="#f8cb0c" strokeWidth={2} name="Avg Duration (s)" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Message Distribution */}
        <Card className="shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">Message Distribution</CardTitle>
            <CardDescription className="text-xs">Breakdown of message types today</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={mockMessageData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {mockMessageData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Appointment Status */}
        <Card className="shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">Appointment Status</CardTitle>
            <CardDescription className="text-xs">Current status of today's appointments</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2 space-y-3">
            {mockAppointmentData.map((item) => (
              <div key={item.status} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div 
                    className="w-2 h-2 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-xs font-medium">{item.status}</span>
                </div>
                <Badge variant="secondary" className="text-xs h-5 min-w-[1.5rem] flex items-center justify-center">{item.count}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* System Status */}
        <Card className="shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">System Status</CardTitle>
            <CardDescription className="text-xs">Current system health and performance</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2 space-y-3">
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span>WhatsApp API</span>
                <span className="text-green-600 font-medium">Online</span>
              </div>
              <Progress value={100} className="h-1.5" />
            </div>
            
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span>Call System</span>
                <span className="text-green-600 font-medium">Online</span>
              </div>
              <Progress value={98} className="h-1.5" />
            </div>
            
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span>Database</span>
                <span className="text-yellow-600 font-medium">Optimizing</span>
              </div>
              <Progress value={85} className="h-1.5" />
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">Recent Activity</CardTitle>
            <CardDescription className="text-xs">Latest system events and updates</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="space-y-3 max-h-60 overflow-y-auto custom-scrollbar">
              {mockRecentActivity.map((activity) => {
                const getIcon = (type) => {
                  switch (type) {
                    case 'call': return Phone;
                    case 'whatsapp': return MessageSquare;
                    case 'appointment': return Calendar;
                    default: return Activity;
                  }
                };
                
                const getStatusColor = (status) => {
                  switch (status) {
                    case 'success': return 'text-green-600';
                    case 'warning': return 'text-yellow-600';
                    case 'error': return 'text-red-600';
                    default: return 'text-blue-600';
                  }
                };

                const Icon = getIcon(activity.type);
                
                return (
                  <div key={activity.id} className="flex items-start space-x-2">
                    <div className={`p-1 rounded-full ${getStatusColor(activity.status)}`}>
                      <Icon className="h-3 w-3" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-900">{activity.message}</p>
                      <p className="text-xs text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
      </div>
    </div>
  );
}


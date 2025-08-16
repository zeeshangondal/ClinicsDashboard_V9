import { useState, useEffect } from 'react';
import { 
  Phone, 
  PhoneCall, 
  PhoneIncoming, 
  PhoneOutgoing, 
  Clock, 
  User, 
  Calendar,
  Filter,
  Download,
  Search,
  Play,
  Pause,
  MoreHorizontal,
  CheckCircle,
  XCircle,
  AlertCircle,
  TrendingUp,
  TrendingDown
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from './ui/table';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from './ui/dropdown-menu';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import authService from '../lib/auth';

// Mock call data
const mockCalls = [
  {
    id: 1,
    phone_number: '+1234567890',
    contact_name: 'John Doe',
    direction: 'outbound',
    status: 'completed',
    duration: 245,
    start_time: '2024-01-15T10:30:00Z',
    end_time: '2024-01-15T10:34:05Z',
    lead_status: 'interested',
    notes: 'Patient interested in dental consultation',
    recording_url: null,
    ai_summary: 'Patient inquired about teeth cleaning appointment. Scheduled for next week.',
    is_currently_calling: false
  },
  {
    id: 2,
    phone_number: '+0987654321',
    contact_name: 'Jane Smith',
    direction: 'inbound',
    status: 'missed',
    duration: 0,
    start_time: '2024-01-15T11:15:00Z',
    end_time: null,
    lead_status: 'new',
    notes: null,
    recording_url: null,
    ai_summary: null,
    is_currently_calling: false
  },
  {
    id: 3,
    phone_number: '+1122334455',
    contact_name: 'Mike Johnson',
    direction: 'outbound',
    status: 'in_progress',
    duration: 120,
    start_time: '2024-01-15T12:00:00Z',
    end_time: null,
    lead_status: 'contacted',
    notes: 'Follow-up call for appointment confirmation',
    recording_url: null,
    ai_summary: null,
    is_currently_calling: true
  },
  {
    id: 4,
    phone_number: '+5566778899',
    contact_name: 'Sarah Wilson',
    direction: 'outbound',
    status: 'failed',
    duration: 0,
    start_time: '2024-01-15T09:45:00Z',
    end_time: '2024-01-15T09:45:15Z',
    lead_status: 'do_not_call',
    notes: 'Number disconnected',
    recording_url: null,
    ai_summary: null,
    is_currently_calling: false
  }
];

const callStats = {
  total_today: 47,
  completed_today: 32,
  missed_today: 8,
  failed_today: 7,
  average_duration: 180,
  success_rate: 68,
  total_change: 12.5,
  completed_change: 8.2,
  missed_change: -3.5,
  duration_change: 5.7
};

export default function CallData() {
  const [calls, setCalls] = useState(mockCalls);
  const [stats, setStats] = useState(callStats);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [directionFilter, setDirectionFilter] = useState('all');
  const [callReasonFilter, setCallReasonFilter] = useState('all');
  const [callReasons, setCallReasons] = useState([]);
  const [currentlyPlaying, setCurrentlyPlaying] = useState(null);

  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  useEffect(() => {
    fetchCallData();
    fetchCallReasons();
  }, []);

  const fetchCallReasons = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/calls/reasons`, {
        headers: {
          Authorization: `Bearer ${authService.getToken()}`,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setCallReasons(data.call_reasons);
      } else {
        console.error("Failed to fetch call reasons:", data.message);
      }
    } catch (error) {
      console.error("Error fetching call reasons:", error);
    }
  };

  const fetchCallData = async () => {
    setLoading(true);
    try {
      // In real app, make API call here
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCalls(mockCalls);
      setStats(callStats);
    } catch (error) {
      console.error('Failed to fetch call data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'missed':
        return <XCircle className="h-4 w-4 text-red-600" />;
      case 'in_progress':
        return <AlertCircle className="h-4 w-4 text-blue-600" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-600" />;
      default:
        return <Phone className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      completed: 'bg-green-100 text-green-800',
      missed: 'bg-red-100 text-red-800',
      in_progress: 'bg-blue-100 text-blue-800',
      failed: 'bg-gray-100 text-gray-800'
    };
    
    return (
      <Badge className={variants[status] || 'bg-gray-100 text-gray-800'}>
        {status.replace('_', ' ').toUpperCase()}
      </Badge>
    );
  };

  const getLeadStatusBadge = (status) => {
    const variants = {
      interested: 'bg-green-100 text-green-800',
      contacted: 'bg-blue-100 text-blue-800',
      not_interested: 'bg-red-100 text-red-800',
      do_not_call: 'bg-red-100 text-red-800',
      new: 'bg-yellow-100 text-yellow-800'
    };
    
    return (
      <Badge className={variants[status] || 'bg-gray-100 text-gray-800'}>
        {status.replace('_', ' ').toUpperCase()}
      </Badge>
    );
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const handleLeadStatusChange = async (callId, newStatus) => {
    try {
      // Update local state
      setCalls(prevCalls => 
        prevCalls.map(call => 
          call.id === callId 
            ? { ...call, lead_status: newStatus }
            : call
        )
      );
      
      // In real app, make API call here
      console.log(`Updated call ${callId} lead status to ${newStatus}`);
    } catch (error) {
      console.error('Failed to update lead status:', error);
    }
  };

  const filteredCalls = calls.filter(call => {
    const matchesSearch = !searchQuery || 
      call.contact_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      call.phone_number.includes(searchQuery);
    
    const matchesStatus = statusFilter === 'all' || call.status === statusFilter;
    const matchesDirection = directionFilter === 'all' || call.direction === directionFilter;
    const matchesCallReason = callReasonFilter === 'all' || call.call_type === callReasonFilter;
    
    return matchesSearch && matchesStatus && matchesDirection && matchesCallReason;
  });

  const StatCard = ({ title, value, change, icon: Icon, color = 'blue', suffix = '' }) => {
    const isPositive = change > 0;
    const isNegative = change < 0;
    const isNeutral = change === 0;
    
    // For missed calls, negative change is positive (fewer missed calls is good)
    const isMissedCalls = title.toLowerCase().includes('missed');
    const effectiveIsPositive = isMissedCalls ? isNegative : isPositive;
    const effectiveIsNegative = isMissedCalls ? isPositive : isNegative;
    
    const colorClasses = {
      blue: 'bg-blue-50 text-blue-600',
      green: 'bg-green-50 text-green-600',
      red: 'bg-red-50 text-red-600',
      yellow: 'bg-yellow-50 text-yellow-600'
    };

    return (
      <Card className="shadow-sm border border-gray-100">
        <CardContent className="p-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600">{title}</p>
              <p className="text-xl font-bold text-gray-900 mt-0.5">{value}{suffix}</p>
              <div className="flex items-center mt-1">
                {effectiveIsPositive && (
                  <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                )}
                {effectiveIsNegative && (
                  <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                )}
                {isNeutral && (
                  <span className="h-3 w-3 bg-gray-300 rounded-full mr-1" />
                )}
                <span className={`text-xs font-medium ${
                  effectiveIsPositive ? 'text-green-600' : 
                  effectiveIsNegative ? 'text-red-600' : 
                  'text-gray-500'
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

  return (
    <div className="p-4 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Call Data</h2>
          <p className="text-sm text-gray-600">Monitor and manage all call activities</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={fetchCallData} disabled={loading} className="h-8 text-xs">
            <Phone className="h-3.5 w-3.5 mr-1.5" />
            Refresh
          </Button>
          <Button variant="outline" size="sm" className="h-8 text-xs">
            <Download className="h-3.5 w-3.5 mr-1.5" />
            Export
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Calls Today"
          value={stats.total_today}
          change={stats.total_change}
          icon={Phone}
          color="blue"
        />
        <StatCard
          title="Completed Calls"
          value={stats.completed_today}
          change={stats.completed_change}
          icon={CheckCircle}
          color="green"
        />
        <StatCard
          title="Missed Calls"
          value={stats.missed_today}
          change={stats.missed_change}
          icon={XCircle}
          color="red"
        />
        <StatCard
          title="Average Duration"
          value={formatDuration(stats.average_duration)}
          change={stats.duration_change}
          icon={Clock}
          color="yellow"
        />
      </div>

      {/* Filters and Search */}
      <Card className="shadow-sm">
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-base">Call History</CardTitle>
          <CardDescription className="text-xs">View and manage all call records</CardDescription>
        </CardHeader>
        <CardContent className="p-4 pt-2">
          <div className="flex flex-col md:flex-row gap-3 mb-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                <Input
                  placeholder="Search by name or phone number..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-8 h-8 text-xs"
                />
              </div>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-32 h-8 text-xs">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all" className="text-xs">All Status</SelectItem>
                <SelectItem value="completed" className="text-xs">Completed</SelectItem>
                <SelectItem value="missed" className="text-xs">Missed</SelectItem>
                <SelectItem value="in_progress" className="text-xs">In Progress</SelectItem>
                <SelectItem value="failed" className="text-xs">Failed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={directionFilter} onValueChange={setDirectionFilter}>
              <SelectTrigger className="w-32 h-8 text-xs">
                <SelectValue placeholder="Direction" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all" className="text-xs">All Calls</SelectItem>
                <SelectItem value="inbound" className="text-xs">Inbound</SelectItem>
                <SelectItem value="outbound" className="text-xs">Outbound</SelectItem>
              </SelectContent>
            </Select>
            <Select value={callReasonFilter} onValueChange={setCallReasonFilter}>
              <SelectTrigger className="w-40 h-8 text-xs">
                <SelectValue placeholder="Call Reason" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all" className="text-xs">All Reasons</SelectItem>
                {callReasons.map((reason) => (
                  <SelectItem key={reason} value={reason} className="text-xs">
                    {reason}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Call Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-xs">Contact</TableHead>
                  <TableHead className="text-xs">Direction</TableHead>
                  <TableHead className="text-xs">Status</TableHead>
                  <TableHead className="text-xs">Duration</TableHead>
                  <TableHead className="text-xs">Start Time</TableHead>
                  <TableHead className="text-xs">Call Reason</TableHead>
                  <TableHead className="text-xs">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCalls.map((call) => (
                  <TableRow key={call.id} className={call.is_currently_calling ? 'bg-blue-50' : ''}>
                    <TableCell className="text-xs">
                      <div className="flex items-center space-x-2">
                        {call.is_currently_calling && (
                          <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                        )}
                        <div>
                          <div className="font-medium">{call.contact_name || 'Unknown'}</div>
                          <div className="text-xs text-gray-500">{call.phone_number}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-xs">
                      <div className="flex items-center space-x-1">
                        {call.direction === 'inbound' ? (
                          <PhoneIncoming className="h-3.5 w-3.5 text-green-600" />
                        ) : (
                          <PhoneOutgoing className="h-3.5 w-3.5 text-blue-600" />
                        )}
                        <span className="capitalize">{call.direction}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-xs">
                      <div className="flex items-center space-x-1">
                        {getStatusIcon(call.status)}
                        {getStatusBadge(call.status)}
                      </div>
                    </TableCell>
                    <TableCell className="text-xs">
                      {formatDuration(call.duration)}
                    </TableCell>
                    <TableCell className="text-xs">
                      {formatDateTime(call.start_time)}
                    </TableCell>
                    <TableCell className="text-xs">
                      <Badge variant="outline" className="text-xs">
                        {call.call_type || 'Not specified'}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-xs">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-7 w-7">
                            <MoreHorizontal className="h-3.5 w-3.5" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel className="text-xs">Lead Status</DropdownMenuLabel>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem onClick={() => handleLeadStatusChange(call.id, 'interested')} className="text-xs">
                            Mark as Interested
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleLeadStatusChange(call.id, 'not_interested')} className="text-xs">
                            Mark as Not Interested
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => handleLeadStatusChange(call.id, 'do_not_call')} className="text-xs">
                            Do Not Call
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem className="text-xs">View Details</DropdownMenuItem>
                          {call.recording_url && (
                            <DropdownMenuItem className="text-xs">Play Recording</DropdownMenuItem>
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {filteredCalls.length === 0 && (
            <div className="text-center py-6">
              <Phone className="h-10 w-10 text-gray-400 mx-auto mb-3" />
              <p className="text-xs text-gray-500">No calls found matching your criteria</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}


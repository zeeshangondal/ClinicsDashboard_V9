import { useState, useEffect } from 'react';
import { 
  Phone, 
  PhoneCall, 
  PhoneOutgoing,
  Upload, 
  Download, 
  Play, 
  Pause, 
  Square,
  User, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Search,
  Filter,
  Plus,
  Edit,
  Trash2,
  MoreHorizontal,
  FileText,
  Users,
  Target,
  TrendingUp,
  TrendingDown,
  Eye
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
import { Progress } from './ui/progress';
import authService from '../lib/auth';

// Mock lead lists data
const mockLeadLists = [
  {
    id: 1,
    name: 'Dental Consultation Leads',
    description: 'Potential patients interested in dental consultations',
    total_leads: 150,
    called_leads: 89,
    completed_calls: 67,
    interested_leads: 23,
    not_interested: 31,
    do_not_call: 8,
    pending_calls: 61,
    created_at: '2024-01-10T09:00:00Z',
    status: 'active',
    campaign_type: 'consultation'
  },
  {
    id: 2,
    name: 'Teeth Whitening Campaign',
    description: 'Follow-up calls for teeth whitening service',
    total_leads: 75,
    called_leads: 45,
    completed_calls: 38,
    interested_leads: 12,
    not_interested: 18,
    do_not_call: 3,
    pending_calls: 30,
    created_at: '2024-01-12T14:30:00Z',
    status: 'active',
    campaign_type: 'service'
  },
  {
    id: 3,
    name: 'Appointment Reminders',
    description: 'Reminder calls for upcoming appointments',
    total_leads: 45,
    called_leads: 45,
    completed_calls: 42,
    interested_leads: 38,
    not_interested: 2,
    do_not_call: 0,
    pending_calls: 0,
    created_at: '2024-01-14T10:00:00Z',
    status: 'completed',
    campaign_type: 'reminder'
  }
];

// Mock individual leads data
const mockLeads = [
  {
    id: 1,
    list_id: 1,
    name: 'John Smith',
    phone_number: '+1234567890',
    email: 'john.smith@email.com',
    status: 'completed',
    call_status: 'interested',
    call_attempts: 2,
    last_call_time: '2024-01-15T14:30:00Z',
    notes: 'Interested in consultation next week',
    priority: 'high',
    created_at: '2024-01-10T09:00:00Z',
    is_currently_calling: false
  },
  {
    id: 2,
    list_id: 1,
    name: 'Jane Doe',
    phone_number: '+0987654321',
    email: 'jane.doe@email.com',
    status: 'in_progress',
    call_status: 'calling',
    call_attempts: 1,
    last_call_time: '2024-01-15T16:00:00Z',
    notes: 'Currently being called by AI',
    priority: 'medium',
    created_at: '2024-01-10T09:15:00Z',
    is_currently_calling: true
  },
  {
    id: 3,
    list_id: 1,
    name: 'Mike Wilson',
    phone_number: '+1122334455',
    email: 'mike.wilson@email.com',
    status: 'pending',
    call_status: 'not_called',
    call_attempts: 0,
    last_call_time: null,
    notes: 'High priority lead from website',
    priority: 'high',
    created_at: '2024-01-10T09:30:00Z',
    is_currently_calling: false
  },
  {
    id: 4,
    list_id: 1,
    name: 'Sarah Johnson',
    phone_number: '+5566778899',
    email: 'sarah.johnson@email.com',
    status: 'completed',
    call_status: 'do_not_call',
    call_attempts: 1,
    last_call_time: '2024-01-14T11:00:00Z',
    notes: 'Requested to be removed from calling list',
    priority: 'low',
    created_at: '2024-01-10T10:00:00Z',
    is_currently_calling: false
  }
];

const outboundStats = {
  total_campaigns: 12,
  active_campaigns: 8,
  total_leads: 1250,
  calls_today: 89,
  success_rate: 34,
  average_call_duration: 145,
  campaigns_change: 15.3,
  leads_change: 8.7,
  calls_change: 22.5,
  success_change: 4.2
};

export default function OutboundCalls() {
  const [leadLists, setLeadLists] = useState(mockLeadLists);
  const [leads, setLeads] = useState(mockLeads);
  const [selectedList, setSelectedList] = useState(null);
  const [stats, setStats] = useState(outboundStats);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [activeTab, setActiveTab] = useState("campaigns");
  const [callTypeFilter, setCallTypeFilter] = useState("all");
  const [callTypes, setCallTypes] = useState([]);

  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  useEffect(() => {
    fetchOutboundData();
    fetchCallTypes();
  }, []);

  const fetchCallTypes = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/calls/types`, {
        headers: {
          Authorization: `Bearer ${authService.getToken()}`,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setCallTypes(data.call_types);
      } else {
        console.error("Failed to fetch call types:", data.message);
      }
    } catch (error) {
      console.error("Error fetching call types:", error);
    }
  };

  const fetchOutboundData = async () => {
    setLoading(true);
    try {
      // In real app, make API call here
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLeadLists(mockLeadLists);
      setLeads(mockLeads);
      setStats(outboundStats);
    } catch (error) {
      console.error('Failed to fetch outbound data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      active: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      paused: 'bg-yellow-100 text-yellow-800',
      draft: 'bg-gray-100 text-gray-800'
    };
    
    return (
      <Badge className={variants[status] || 'bg-gray-100 text-gray-800'}>
        {status.toUpperCase()}
      </Badge>
    );
  };

  const getCallStatusBadge = (status) => {
    const variants = {
      interested: 'bg-green-100 text-green-800',
      not_interested: 'bg-red-100 text-red-800',
      do_not_call: 'bg-red-100 text-red-800',
      calling: 'bg-blue-100 text-blue-800',
      not_called: 'bg-gray-100 text-gray-800',
      failed: 'bg-orange-100 text-orange-800'
    };
    
    return (
      <Badge className={variants[status] || 'bg-gray-100 text-gray-800'}>
        {status.replace('_', ' ').toUpperCase()}
      </Badge>
    );
  };

  const getPriorityBadge = (priority) => {
    const variants = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800'
    };
    
    return (
      <Badge className={variants[priority] || 'bg-gray-100 text-gray-800'}>
        {priority.toUpperCase()}
      </Badge>
    );
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const calculateProgress = (called, total) => {
    return total > 0 ? Math.round((called / total) * 100) : 0;
  };

  const handleLeadStatusChange = async (leadId, newStatus) => {
    try {
      // Update local state
      setLeads(prevLeads => 
        prevLeads.map(lead => 
          lead.id === leadId 
            ? { ...lead, call_status: newStatus, status: newStatus === 'do_not_call' ? 'completed' : lead.status }
            : lead
        )
      );
      
      // In real app, make API call here
      console.log(`Updated lead ${leadId} status to ${newStatus}`);
    } catch (error) {
      console.error('Failed to update lead status:', error);
    }
  };

  const handleCampaignAction = async (listId, action) => {
    try {
      // Update local state based on action
      if (action === 'start') {
        setLeadLists(prevLists => 
          prevLists.map(list => 
            list.id === listId 
              ? { ...list, status: 'active' }
              : list
          )
        );
      } else if (action === 'pause') {
        setLeadLists(prevLists => 
          prevLists.map(list => 
            list.id === listId 
              ? { ...list, status: 'paused' }
              : list
          )
        );
      }
      
      // In real app, make API call here
      console.log(`${action} campaign ${listId}`);
    } catch (error) {
      console.error(`Failed to ${action} campaign:`, error);
    }
  };

  const filteredLeads = leads.filter(lead => {
    if (selectedList && lead.list_id !== selectedList.id) return false;
    
    const matchesSearch = !searchQuery || 
      lead.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      lead.phone_number.includes(searchQuery) ||
      lead.email?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || lead.call_status === statusFilter;
    const matchesPriority = priorityFilter === 'all' || lead.priority === priorityFilter;
    const matchesCallType = callTypeFilter === 'all' || lead.call_type === callTypeFilter;
    
    return matchesSearch && matchesStatus && matchesPriority && matchesCallType;
  });

  const StatCard = ({ title, value, change, icon: Icon, color = 'blue', suffix = '' }) => {
    const isPositive = change > 0;
    const isNegative = change < 0;
    const isNeutral = change === 0;
    
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
              <p className="text-xl font-bold text-gray-900 mt-0.5">{value}{suffix}</p>
              <div className="flex items-center mt-1">
                {isPositive && (
                  <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                )}
                {isNegative && (
                  <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                )}
                {isNeutral && (
                  <span className="h-3 w-3 bg-gray-300 rounded-full mr-1" />
                )}
                <span className={`text-xs font-medium ${
                  isPositive ? 'text-green-600' : 
                  isNegative ? 'text-red-600' : 
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
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Active Campaigns"
          value={stats.active_campaigns}
          change={stats.campaigns_change}
          icon={Target}
          color="blue"
        />
        <StatCard
          title="Total Leads"
          value={stats.total_leads}
          change={stats.leads_change}
          icon={Users}
          color="green"
        />
        <StatCard
          title="Calls Today"
          value={stats.calls_today}
          change={stats.calls_change}
          icon={PhoneOutgoing}
          color="yellow"
        />
        <StatCard
          title="Success Rate"
          value={stats.success_rate}
          change={stats.success_change}
          icon={TrendingUp}
          color="purple"
          suffix="%"
        />
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="campaigns" className="text-xs">Lead Lists & Campaigns</TabsTrigger>
          <TabsTrigger value="leads" className="text-xs">Individual Leads</TabsTrigger>
        </TabsList>

        {/* Campaigns Tab */}
        <TabsContent value="campaigns">
          <Card className="shadow-sm">
            <CardHeader className="p-4 pb-2">
              <CardTitle className="text-base">Lead Lists & Campaigns</CardTitle>
              <CardDescription className="text-xs">Manage your outbound calling campaigns</CardDescription>
            </CardHeader>
            <CardContent className="p-4">
              <div className="grid gap-4">
                {leadLists.map((list) => (
                  <Card key={list.id} className="border-l-4 border-l-primary shadow-sm">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <h3 className="text-base font-semibold">{list.name}</h3>
                            {getStatusBadge(list.status)}
                            <Badge variant="outline" className="text-[10px]">
                              {list.campaign_type.toUpperCase()}
                            </Badge>
                          </div>
                          <p className="text-xs text-gray-600 mb-2">{list.description}</p>
                          <p className="text-[10px] text-gray-500">Created: {formatDateTime(list.created_at)}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => setSelectedList(list)}
                            className="h-7 text-xs"
                          >
                            <Eye className="h-3.5 w-3.5 mr-1.5" />
                            View Leads
                          </Button>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="icon" className="h-7 w-7">
                                <MoreHorizontal className="h-3.5 w-3.5" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuLabel className="text-xs">Campaign Actions</DropdownMenuLabel>
                              <DropdownMenuSeparator />
                              {list.status === 'active' ? (
                                <DropdownMenuItem onClick={() => handleCampaignAction(list.id, 'pause')} className="text-xs">
                                  <Pause className="h-3.5 w-3.5 mr-2" />
                                  Pause Campaign
                                </DropdownMenuItem>
                              ) : (
                                <DropdownMenuItem onClick={() => handleCampaignAction(list.id, 'start')} className="text-xs">
                                  <Play className="h-3.5 w-3.5 mr-2" />
                                  Start Campaign
                                </DropdownMenuItem>
                              )}
                              <DropdownMenuItem className="text-xs">
                                <Upload className="h-3.5 w-3.5 mr-2" />
                                Upload Leads
                              </DropdownMenuItem>
                              <DropdownMenuItem className="text-xs">
                                <Download className="h-3.5 w-3.5 mr-2" />
                                Export Results
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem className="text-xs">
                                <Edit className="h-3.5 w-3.5 mr-2" />
                                Edit Campaign
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </div>
                      </div>

                      {/* Progress and Stats */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-600">{list.total_leads}</div>
                          <div className="text-[10px] text-gray-500">Total Leads</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-green-600">{list.called_leads}</div>
                          <div className="text-[10px] text-gray-500">Called</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-yellow-600">{list.interested_leads}</div>
                          <div className="text-[10px] text-gray-500">Interested</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-red-600">{list.pending_calls}</div>
                          <div className="text-[10px] text-gray-500">Pending</div>
                        </div>
                      </div>

                      {/* Progress Bar */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span>Campaign Progress</span>
                          <span>{calculateProgress(list.called_leads, list.total_leads)}%</span>
                        </div>
                        <Progress 
                          value={calculateProgress(list.called_leads, list.total_leads)} 
                          className="h-2"
                        />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {leadLists.length === 0 && (
                <div className="text-center py-6">
                  <Target className="h-10 w-10 text-gray-400 mx-auto mb-3" />
                  <p className="text-xs text-gray-500">No campaigns found</p>
                  <Button size="sm" className="mt-3 craft-ai-teal h-8 text-xs">
                    <Plus className="h-3.5 w-3.5 mr-1.5" />
                    Create First Campaign
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Leads Tab */}
        <TabsContent value="leads">
          <Card className="shadow-sm">
            <CardHeader className="p-4 pb-2">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base">Individual Leads</CardTitle>
                  <CardDescription className="text-xs">
                    {selectedList 
                      ? `Viewing leads from: ${selectedList.name}`
                      : 'View and manage individual leads'
                    }
                  </CardDescription>
                </div>
                {selectedList && (
                  <Button 
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedList(null)}
                    className="h-7 text-xs"
                  >
                    View All Leads
                  </Button>
                )}
              </div>
              
              {/* Filters */}
              <div className="flex flex-col md:flex-row gap-3 mt-2">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                    <Input
                      placeholder="Search by name, phone, or email..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-8 h-8 text-xs"
                    />
                  </div>
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-32 h-8 text-xs">
                    <SelectValue placeholder="Call Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all" className="text-xs">All Status</SelectItem>
                    <SelectItem value="not_called" className="text-xs">Not Called</SelectItem>
                    <SelectItem value="calling" className="text-xs">Calling</SelectItem>
                    <SelectItem value="interested" className="text-xs">Interested</SelectItem>
                    <SelectItem value="not_interested" className="text-xs">Not Interested</SelectItem>
                    <SelectItem value="do_not_call" className="text-xs">Do Not Call</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                  <SelectTrigger className="w-32 h-8 text-xs">
                    <SelectValue placeholder="Priority" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all" className="text-xs">All Priority</SelectItem>
                    <SelectItem value="high" className="text-xs">High</SelectItem>
                    <SelectItem value="medium" className="text-xs">Medium</SelectItem>
                    <SelectItem value="low" className="text-xs">Low</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={callTypeFilter} onValueChange={setCallTypeFilter}>
                  <SelectTrigger className="w-32 h-8 text-xs">
                    <SelectValue placeholder="Call Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all" className="text-xs">All Call Types</SelectItem>
                    {callTypes.map((type) => (
                      <SelectItem key={type} value={type} className="text-xs">
                        {type.replace(/_/g, " ").split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(" ")}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardHeader>
            <CardContent className="p-4">
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="text-xs">Contact</TableHead>
                      <TableHead className="text-xs">Priority</TableHead>
                      <TableHead className="text-xs">Call Status</TableHead>
                      <TableHead className="text-xs">Attempts</TableHead>
                      <TableHead className="text-xs">Last Call</TableHead>
                      <TableHead className="text-xs">Notes</TableHead>
                      <TableHead className="text-xs">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredLeads.map((lead) => (
                      <TableRow key={lead.id} className={lead.is_currently_calling ? 'bg-blue-50' : ''}>
                        <TableCell className="text-xs">
                          <div className="flex items-center space-x-2">
                            {lead.is_currently_calling && (
                              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                            )}
                            <div>
                              <div className="font-medium">{lead.name}</div>
                              <div className="text-xs text-gray-500">{lead.phone_number}</div>
                              {lead.email && (
                                <div className="text-xs text-gray-500">{lead.email}</div>
                              )}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell className="text-xs">
                          {getPriorityBadge(lead.priority)}
                        </TableCell>
                        <TableCell className="text-xs">
                          {getCallStatusBadge(lead.call_status)}
                        </TableCell>
                        <TableCell className="text-xs">
                          <div className="flex items-center space-x-1">
                            <PhoneCall className="h-3.5 w-3.5 text-gray-400" />
                            <span>{lead.call_attempts}</span>
                          </div>
                        </TableCell>
                        <TableCell className="text-xs">
                          {formatDateTime(lead.last_call_time)}
                        </TableCell>
                        <TableCell className="text-xs">
                          <div className="max-w-xs truncate">
                            {lead.notes || '-'}
                          </div>
                        </TableCell>
                        <TableCell className="text-xs">
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="icon" className="h-7 w-7">
                                <MoreHorizontal className="h-3.5 w-3.5" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuLabel className="text-xs">Lead Actions</DropdownMenuLabel>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem onClick={() => handleLeadStatusChange(lead.id, 'interested')} className="text-xs">
                                <CheckCircle className="h-3.5 w-3.5 mr-2" />
                                Mark Interested
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => handleLeadStatusChange(lead.id, 'not_interested')} className="text-xs">
                                <XCircle className="h-3.5 w-3.5 mr-2" />
                                Not Interested
                              </DropdownMenuItem>
                              <DropdownMenuItem onClick={() => handleLeadStatusChange(lead.id, 'do_not_call')} className="text-xs">
                                <XCircle className="h-3.5 w-3.5 mr-2" />
                                Do Not Call
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem className="text-xs">
                                <Phone className="h-3.5 w-3.5 mr-2" />
                                Manual Call
                              </DropdownMenuItem>
                              <DropdownMenuItem className="text-xs">
                                <Edit className="h-3.5 w-3.5 mr-2" />
                                Edit Lead
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              {filteredLeads.length === 0 && (
                <div className="text-center py-6">
                  <Users className="h-10 w-10 text-gray-400 mx-auto mb-3" />
                  <p className="text-xs text-gray-500">No leads found matching your criteria</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}


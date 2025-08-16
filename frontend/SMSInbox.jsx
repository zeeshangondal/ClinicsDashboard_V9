import { useState, useEffect, useRef } from 'react';
import { 
  MessageSquare, 
  User, 
  Bot, 
  Clock, 
  Search, 
  Filter,
  Download,
  Eye,
  MessageCircle,
  Phone,
  Calendar,
  MoreHorizontal,
  CheckCircle,
  AlertCircle,
  UserCheck,
  TrendingUp,
  TrendingDown,
  Send,
  Paperclip,
  Smile
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from './ui/card';
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
import { ScrollArea } from './ui/scroll-area';
import { Textarea } from './ui/textarea';
import authService from '../lib/auth';

// Mock SMS conversation data
const mockConversations = [
  {
    id: 1,
    contact_name: 'Michael Brown',
    phone_number: '+1234567890',
    last_message: 'I received your appointment reminder. Thanks!',
    last_message_time: '2024-01-15T14:30:00Z',
    message_count: 9,
    unread_count: 0,
    status: 'resolved',
    assigned_agent: 'Sarah Wilson',
    handoff_time: '2024-01-15T13:45:00Z',
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    id: 2,
    contact_name: 'Emily Davis',
    phone_number: '+1987654321',
    last_message: 'Can I get directions to your office?',
    last_message_time: '2024-01-15T15:15:00Z',
    message_count: 5,
    unread_count: 2,
    status: 'active',
    assigned_agent: null,
    handoff_time: null,
    created_at: '2024-01-15T14:30:00Z'
  },
  {
    id: 3,
    contact_name: 'David Wilson',
    phone_number: '+1122334455',
    last_message: 'Do I need to bring anything for my first visit?',
    last_message_time: '2024-01-15T16:00:00Z',
    message_count: 1,
    unread_count: 1,
    status: 'pending_handoff',
    assigned_agent: null,
    handoff_time: null,
    created_at: '2024-01-15T15:45:00Z'
  }
];

// Mock message data for conversations
const mockMessages = [
  {
    id: 1,
    conversation_id: 1,
    message_text: 'Hello, this is a reminder about your dental appointment tomorrow at 2:00 PM with Dr. Martinez. Reply Y to confirm or N to reschedule.',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T10:00:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 2,
    conversation_id: 1,
    message_text: 'Y',
    sender_type: 'customer',
    sender_name: 'Michael Brown',
    timestamp: '2024-01-15T10:30:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 3,
    conversation_id: 1,
    message_text: 'Thank you for confirming your appointment. We look forward to seeing you tomorrow at 2:00 PM. Please arrive 15 minutes early to complete any necessary paperwork.',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T10:31:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 4,
    conversation_id: 1,
    message_text: 'Do I need to bring anything specific?',
    sender_type: 'customer',
    sender_name: 'Michael Brown',
    timestamp: '2024-01-15T11:00:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 5,
    conversation_id: 1,
    message_text: 'Please bring your ID, insurance card, and a list of any medications you are currently taking. If you have had any recent dental X-rays from another provider, those would be helpful as well.',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T11:02:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 6,
    conversation_id: 1,
    message_text: 'Let me transfer you to our front desk staff who can provide more specific information about your visit.',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T13:44:00Z',
    message_type: 'system',
    is_read: true
  },
  {
    id: 7,
    conversation_id: 1,
    message_text: 'Hi Michael, this is Sarah from the front desk. In addition to what was mentioned, if you have any dental concerns or specific areas you want the dentist to check, please make a note of them so we can address them during your appointment.',
    sender_type: 'human',
    sender_name: 'Sarah Wilson',
    timestamp: '2024-01-15T13:45:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 8,
    conversation_id: 1,
    message_text: 'I received your appointment reminder. Thanks!',
    sender_type: 'customer',
    sender_name: 'Michael Brown',
    timestamp: '2024-01-15T14:30:00Z',
    message_type: 'text',
    is_read: true
  }
];

const mockMessagesConv2 = [
  {
    id: 9,
    conversation_id: 2,
    message_text: 'Hi, I have an appointment next week but I need directions to your office.',
    sender_type: 'customer',
    sender_name: 'Emily Davis',
    timestamp: '2024-01-15T14:30:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 10,
    conversation_id: 2,
    message_text: 'Hello Emily! Our office is located at 123 Main Street, Suite 200, in downtown. We\'re in the Oakwood Medical Building, across from Central Park. Is there a specific transportation method you\'ll be using?',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T14:31:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 11,
    conversation_id: 2,
    message_text: 'I\'ll be driving. Is there parking available?',
    sender_type: 'customer',
    sender_name: 'Emily Davis',
    timestamp: '2024-01-15T14:32:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 12,
    conversation_id: 2,
    message_text: 'Yes, we have a parking garage attached to our building. We validate parking for patients, so be sure to bring your ticket with you to your appointment. The entrance to the garage is on Oak Street, just past the main building entrance.',
    sender_type: 'ai',
    sender_name: 'Craft AI Assistant',
    timestamp: '2024-01-15T14:33:00Z',
    message_type: 'text',
    is_read: true
  },
  {
    id: 13,
    conversation_id: 2,
    message_text: 'Can I get directions to your office?',
    sender_type: 'customer',
    sender_name: 'Emily Davis',
    timestamp: '2024-01-15T15:15:00Z',
    message_type: 'text',
    is_read: false
  }
];

const mockMessagesConv3 = [
  {
    id: 14,
    conversation_id: 3,
    message_text: 'Do I need to bring anything for my first visit?',
    sender_type: 'customer',
    sender_name: 'David Wilson',
    timestamp: '2024-01-15T16:00:00Z',
    message_type: 'text',
    is_read: false
  }
];

// Quick reply templates
const quickReplyTemplates = [
  "Thank you for your message. How can I assist you today?",
  "Your appointment has been confirmed for [date/time].",
  "We're located at 123 Main Street, Suite 200, in the Oakwood Medical Building.",
  "Please bring your ID, insurance card, and a list of current medications.",
  "Would you like me to connect you with a staff member for more assistance?"
];

const smsStats = {
  total_conversations: 124,
  active_conversations: 18,
  pending_handoff: 5,
  resolved_today: 36,
  average_response_time: 85,
  ai_resolution_rate: 72,
  total_change: 8.3,
  active_change: 2.1,
  pending_change: -1.5,
  resolution_change: 5.2
};

export default function SMSInbox() {
  const [conversations, setConversations] = useState(mockConversations);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState(smsStats);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [newMessage, setNewMessage] = useState('');
  const [showQuickReplies, setShowQuickReplies] = useState(false);
  
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const user = authService.getCurrentUser();
  const clinic = authService.getCurrentClinic();

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  }, [messages]);

  const fetchConversations = async () => {
    setLoading(true);
    try {
      // In real app, make API call here
      await new Promise(resolve => setTimeout(resolve, 1000));
      setConversations(mockConversations);
      setStats(smsStats);
    } catch (error) {
      console.error('Failed to fetch conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (conversationId) => {
    try {
      // In real app, make API call here
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Select the appropriate mock messages based on conversation ID
      let conversationMessages;
      if (conversationId === 1) {
        conversationMessages = mockMessages;
      } else if (conversationId === 2) {
        conversationMessages = mockMessagesConv2;
      } else if (conversationId === 3) {
        conversationMessages = mockMessagesConv3;
      } else {
        conversationMessages = [];
      }
      
      setMessages(conversationMessages);
      
      // Mark messages as read
      if (conversationId === 2 || conversationId === 3) {
        // Update the conversation to mark messages as read
        setConversations(prevConversations => 
          prevConversations.map(conv => 
            conv.id === conversationId 
              ? { ...conv, unread_count: 0 }
              : conv
          )
        );
      }
    } catch (error) {
      console.error('Failed to fetch messages:', error);
    }
  };

  const handleConversationSelect = (conversation) => {
    setSelectedConversation(conversation);
    fetchMessages(conversation.id);
  };

  const handleSendMessage = () => {
    if (!newMessage.trim() || !selectedConversation) return;
    
    const currentTime = new Date().toISOString();
    const newMessageObj = {
      id: Date.now(), // Use timestamp as temporary ID
      conversation_id: selectedConversation.id,
      message_text: newMessage.trim(),
      sender_type: 'human',
      sender_name: user?.first_name || user?.username || 'Agent',
      timestamp: currentTime,
      message_type: 'text',
      is_read: true
    };
    
    // Add message to the conversation
    setMessages(prevMessages => [...prevMessages, newMessageObj]);
    
    // Update the conversation with the new last message
    setConversations(prevConversations => 
      prevConversations.map(conv => 
        conv.id === selectedConversation.id 
          ? { 
              ...conv, 
              last_message: newMessage.trim(),
              last_message_time: currentTime,
              message_count: conv.message_count + 1,
              status: conv.status === 'pending_handoff' ? 'active' : conv.status,
              assigned_agent: conv.assigned_agent || (user?.first_name || user?.username || 'Agent')
            }
          : conv
      )
    );
    
    // Clear the input
    setNewMessage('');
    setShowQuickReplies(false);
  };

  const handleEndHandoff = (conversationId) => {
    const user = authService.getCurrentUser();
    const currentTime = new Date().toISOString();
    
    // Update conversation status to indicate handoff is complete
    setConversations(prevConversations => 
      prevConversations.map(conv => 
        conv.id === conversationId 
          ? { 
              ...conv, 
              status: 'resolved',
              assigned_agent: user?.first_name || user?.username || 'Agent',
              last_message_time: currentTime,
              handoff_completed_at: currentTime,
              handoff_completed_by: user?.first_name || user?.username || 'Agent'
            }
          : conv
      )
    );

    // Add a system message to indicate handoff completion
    const systemMessage = {
      id: Date.now(),
      conversation_id: conversationId,
      message_text: `Handoff completed by ${user?.first_name || user?.username || 'Agent'}. AI can now take over this conversation.`,
      sender_type: 'system',
      sender_name: 'System',
      timestamp: currentTime,
      message_type: 'system',
      is_read: true
    };
    
    setMessages(prevMessages => [...prevMessages, systemMessage]);
    
    // In a real application, you would make an API call here to notify the backend
    // that the handoff is complete and AI can resume handling this conversation
    console.log(`SMS Handoff completed for conversation ${conversationId} by ${user?.first_name || user?.username || 'Agent'}`);
  };

  const handleQuickReplySelect = (template) => {
    setNewMessage(template);
    setShowQuickReplies(false);
  };

  const getStatusBadge = (status) => {
    const variants = {
      active: 'bg-green-100 text-green-800',
      resolved: 'bg-blue-100 text-blue-800',
      pending_handoff: 'bg-yellow-100 text-yellow-800',
      closed: 'bg-gray-100 text-gray-800'
    };
    
    return (
      <Badge className={variants[status] || 'bg-gray-100 text-gray-800'}>
        {status.replace('_', ' ').toUpperCase()}
      </Badge>
    );
  };

  const getSenderIcon = (senderType) => {
    switch (senderType) {
      case 'ai':
        return <Bot className="h-4 w-4 text-blue-600" />;
      case 'human':
        return <UserCheck className="h-4 w-4 text-green-600" />;
      case 'customer':
        return <User className="h-4 w-4 text-gray-600" />;
      default:
        return <MessageCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatTime = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = !searchQuery || 
      conv.contact_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      conv.phone_number?.includes(searchQuery) ||
      conv.last_message?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || conv.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const StatCard = ({ title, value, change, icon: Icon, color = 'blue', suffix = '' }) => {
    const isPositive = change > 0;
    const isNegative = change < 0;
    const isNeutral = change === 0;
    
    // For pending handoff, negative change is positive (fewer pending handoffs is good)
    const isPendingHandoff = title.toLowerCase().includes('pending handoff');
    const effectiveIsPositive = isPendingHandoff ? isNegative : isPositive;
    const effectiveIsNegative = isPendingHandoff ? isPositive : isNegative;
    
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
          <h2 className="text-xl font-bold text-gray-900">SMS Inbox</h2>
          <p className="text-sm text-gray-600">Monitor all SMS conversations and AI interactions</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={fetchConversations} disabled={loading} className="h-8 text-xs">
            <MessageSquare className="h-3.5 w-3.5 mr-1.5" />
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
          title="SMS Messages"
          value={stats.total_conversations}
          change={stats.total_change}
          icon={MessageSquare}
          color="blue"
        />
        <StatCard
          title="Active Chats"
          value={stats.active_conversations}
          change={stats.active_change}
          icon={MessageCircle}
          color="green"
        />
        <StatCard
          title="Pending Handoff"
          value={stats.pending_handoff}
          change={stats.pending_change}
          icon={AlertCircle}
          color="yellow"
        />
        <StatCard
          title="AI Resolution Rate"
          value={stats.ai_resolution_rate}
          change={stats.resolution_change}
          icon={Bot}
          color="purple"
          suffix="%"
        />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Conversations List */}
        <Card className="lg:col-span-1 shadow-sm">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-base">Conversations</CardTitle>
            <CardDescription className="text-xs">All SMS conversations</CardDescription>
            
            {/* Filters */}
            <div className="space-y-2 mt-2">
              <div className="relative">
                <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                <Input
                  placeholder="Search conversations..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-8 h-8 text-xs"
                />
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="h-8 text-xs">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all" className="text-xs">All Status</SelectItem>
                  <SelectItem value="active" className="text-xs">Active</SelectItem>
                  <SelectItem value="pending_handoff" className="text-xs">Pending Handoff</SelectItem>
                  <SelectItem value="resolved" className="text-xs">Resolved</SelectItem>
                  <SelectItem value="closed" className="text-xs">Closed</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <ScrollArea className="h-80">
              <div className="space-y-2 p-4">
                {filteredConversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedConversation?.id === conversation.id
                        ? 'bg-primary/10 border-primary'
                        : 'hover:bg-gray-50'
                    }`}
                    onClick={() => handleConversationSelect(conversation)}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-xs truncate">
                          {conversation.contact_name || 'Unknown Contact'}
                        </h4>
                        <p className="text-[10px] text-gray-500">{conversation.phone_number}</p>
                      </div>
                      <div className="flex items-center space-x-2 ml-2">
                        {conversation.unread_count > 0 && (
                          <Badge variant="destructive" className="text-[10px]">
                            {conversation.unread_count}
                          </Badge>
                        )}
                        {getStatusBadge(conversation.status)}
                      </div>
                    </div>
                    
                    <p className="text-[10px] text-gray-600 truncate mb-2">
                      {conversation.last_message}
                    </p>
                    
                    <div className="flex items-center justify-between text-[10px] text-gray-500">
                      <span>{formatTime(conversation.last_message_time)}</span>
                      <span>{conversation.message_count} messages</span>
                    </div>
                    
                    {conversation.assigned_agent && (
                      <div className="flex items-center mt-2 text-[10px] text-green-600">
                        <UserCheck className="h-3 w-3 mr-1" />
                        <span>{conversation.assigned_agent}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Message Thread */}
        <Card className="lg:col-span-2 shadow-sm flex flex-col">
          <CardHeader className="p-4 pb-2">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">
                  {selectedConversation 
                    ? `${selectedConversation.contact_name || 'Unknown Contact'}`
                    : 'Select a conversation'
                  }
                </CardTitle>
                <CardDescription className="text-xs">
                  {selectedConversation 
                    ? `${selectedConversation.phone_number} • ${messages.length} messages`
                    : 'Choose a conversation to view messages'
                  }
                </CardDescription>
              </div>
              {selectedConversation && (
                <div className="flex items-center space-x-2">
                  {getStatusBadge(selectedConversation.status)}
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-7 w-7">
                        <MoreHorizontal className="h-3.5 w-3.5" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem className="text-xs">
                        <Phone className="h-3.5 w-3.5 mr-2" />
                        Call Contact
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-xs">
                        <Calendar className="h-3.5 w-3.5 mr-2" />
                        Schedule Appointment
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-xs">
                        <UserCheck className="h-3.5 w-3.5 mr-2" />
                        Assign to Agent
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-xs">
                        <CheckCircle className="h-3.5 w-3.5 mr-2" />
                        Mark as Resolved
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              )}
            </div>
          </CardHeader>
          <CardContent className="p-4 flex-grow overflow-hidden">
            {selectedConversation ? (
              <ScrollArea className="h-64">
                <div className="space-y-3">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.sender_type === 'customer' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[85%] px-3 py-2 rounded-lg break-words ${
                          message.sender_type === 'customer'
                            ? 'bg-primary text-primary-foreground'
                            : message.sender_type === 'ai'
                            ? 'bg-blue-100 text-blue-900'
                            : message.sender_type === 'human'
                            ? 'bg-green-100 text-green-900'
                            : 'bg-gray-100 text-gray-900'
                        }`}
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          {getSenderIcon(message.sender_type)}
                          <span className="text-[10px] font-medium">
                            {message.sender_name}
                          </span>
                        </div>
                        <p className="text-xs whitespace-pre-wrap">{message.message_text}</p>
                        <p className="text-[10px] opacity-70 mt-1">
                          {formatTime(message.timestamp)}
                        </p>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              </ScrollArea>
            ) : (
              <div className="h-64 flex items-center justify-center">
                <div className="text-center">
                  <MessageSquare className="h-10 w-10 text-gray-400 mx-auto mb-3" />
                  <p className="text-xs text-gray-500">Select a conversation to view messages</p>
                </div>
              </div>
            )}
          </CardContent>
          
          {/* Message Input */}
          {selectedConversation && (
            <CardFooter className="p-4 pt-2 border-t">
              <div className="w-full space-y-2">
                {/* Quick Reply Templates */}
                {showQuickReplies && (
                  <div className="bg-gray-50 p-2 rounded-md">
                    <p className="text-xs font-medium mb-1">Quick Replies:</p>
                    <div className="flex flex-wrap gap-1">
                      {quickReplyTemplates.map((template, index) => (
                        <Button 
                          key={index} 
                          variant="outline" 
                          size="sm" 
                          className="text-xs h-7"
                          onClick={() => handleQuickReplySelect(template)}
                        >
                          {template.length > 30 ? template.substring(0, 30) + '...' : template}
                        </Button>
                      ))}
                    </div>
                  </div>
                )}
                
                <div className="flex items-end gap-2">
                  <div className="flex-grow relative">
                    <Textarea
                      placeholder="Type your message..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      className="min-h-[60px] text-xs resize-none pr-8"
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          handleSendMessage();
                        }
                      }}
                    />
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute right-2 bottom-2 h-6 w-6"
                      onClick={() => setShowQuickReplies(!showQuickReplies)}
                    >
                      <Smile className="h-4 w-4 text-gray-400" />
                    </Button>
                  </div>
                  <div className="flex gap-1">
                    <Button variant="outline" size="icon" className="h-9 w-9">
                      <Paperclip className="h-4 w-4" />
                    </Button>
                    <Button 
                      onClick={handleSendMessage}
                      disabled={!newMessage.trim()} 
                      className="h-9 craft-ai-teal"
                    >
                      <Send className="h-4 w-4" />
                    </Button>
                    {selectedConversation?.status === 'pending_handoff' && (
                      <Button 
                        onClick={() => handleEndHandoff(selectedConversation.id)}
                        variant="outline"
                        className="h-9 text-xs px-3 border-green-500 text-green-600 hover:bg-green-50"
                      >
                        <UserCheck className="h-4 w-4 mr-1" />
                        End Handoff
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </CardFooter>
          )}
        </Card>
      </div>
    </div>
  );
}


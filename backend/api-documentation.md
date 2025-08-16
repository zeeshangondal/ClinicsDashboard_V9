# Craft AI Dashboard - API Documentation

This document provides comprehensive documentation for the Craft AI Dashboard REST API.

## 🔗 Base URL

```
Production: https://60h5imcyqzzl.manus.space
Local: http://localhost:5000
```

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### POST /api/auth/login
Login with clinic credentials.

**Request Body:**
```json
{
  "clinicName": "Test Clinic",
  "username": "demo",
  "password": "demo"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "demo",
    "clinicName": "Test Clinic",
    "role": "clinic_admin"
  }
}
```

#### POST /api/auth/logout
Logout and invalidate token.

**Response:**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

#### GET /api/auth/verify
Verify token validity.

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "demo",
    "clinicName": "Test Clinic",
    "role": "clinic_admin"
  }
}
```

## 📊 Dashboard Endpoints

#### GET /api/dashboard/stats
Get dashboard statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "todaysCalls": {
      "value": 47,
      "change": 12.5,
      "trend": "up"
    },
    "whatsappMessages": {
      "value": 156,
      "change": -3.2,
      "trend": "down"
    },
    "appointments": {
      "value": 23,
      "change": 8.7,
      "trend": "up"
    },
    "activeConversations": {
      "value": 12,
      "change": 15.3,
      "trend": "up"
    }
  }
}
```

#### GET /api/dashboard/call-volume
Get call volume data for charts.

**Query Parameters:**
- `period` (optional): `today`, `week`, `month` (default: `today`)

**Response:**
```json
{
  "success": true,
  "data": {
    "labels": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"],
    "values": [120, 180, 240, 200, 160, 220, 190, 150],
    "avgDuration": [5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.3, 4.7]
  }
}
```

#### GET /api/dashboard/message-distribution
Get message distribution data for pie chart.

**Response:**
```json
{
  "success": true,
  "data": [
    { "name": "WhatsApp", "value": 45, "color": "#25D366" },
    { "name": "SMS", "value": 30, "color": "#007ACC" },
    { "name": "Telegram", "value": 25, "color": "#0088CC" }
  ]
}
```

## 📞 Call Data Endpoints

#### GET /api/calls
Get call records.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Records per page (default: 20)
- `date` (optional): Filter by date (YYYY-MM-DD)
- `status` (optional): Filter by status (`completed`, `missed`, `ongoing`)

**Response:**
```json
{
  "success": true,
  "data": {
    "calls": [
      {
        "id": 1,
        "phoneNumber": "+1234567890",
        "contactName": "John Doe",
        "duration": "00:05:23",
        "status": "completed",
        "timestamp": "2025-01-23T10:30:00Z",
        "direction": "inbound"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8
    }
  }
}
```

#### POST /api/calls
Create a new call record.

**Request Body:**
```json
{
  "phoneNumber": "+1234567890",
  "contactName": "John Doe",
  "direction": "outbound",
  "status": "ongoing"
}
```

#### PUT /api/calls/{id}
Update call record.

**Request Body:**
```json
{
  "status": "completed",
  "duration": "00:05:23",
  "notes": "Customer inquiry about services"
}
```

## 💬 WhatsApp Endpoints

#### GET /api/whatsapp/conversations
Get WhatsApp conversations.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "contactName": "Alice Johnson",
      "phoneNumber": "+1234567890",
      "lastMessage": "Thank you for the information!",
      "timestamp": "2025-01-23T14:30:00Z",
      "unreadCount": 0,
      "status": "active"
    }
  ]
}
```

#### GET /api/whatsapp/conversations/{id}/messages
Get messages for a specific conversation.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "conversationId": 1,
      "message": "Hello, I need help with my appointment",
      "sender": "customer",
      "timestamp": "2025-01-23T14:25:00Z",
      "status": "delivered"
    },
    {
      "id": 2,
      "conversationId": 1,
      "message": "Sure! I can help you with that.",
      "sender": "agent",
      "timestamp": "2025-01-23T14:26:00Z",
      "status": "delivered"
    }
  ]
}
```

#### POST /api/whatsapp/conversations/{id}/messages
Send a WhatsApp message.

**Request Body:**
```json
{
  "message": "Thank you for contacting us. How can I help you today?",
  "type": "text"
}
```

**Response:**
```json
{
  "success": true,
  "messageId": "msg_123456789",
  "status": "sent"
}
```

## 📱 SMS Endpoints

#### GET /api/sms/conversations
Get SMS conversations.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "contactName": "Bob Smith",
      "phoneNumber": "+1987654321",
      "lastMessage": "Appointment confirmed for tomorrow",
      "timestamp": "2025-01-23T13:45:00Z",
      "unreadCount": 1,
      "status": "active"
    }
  ]
}
```

#### POST /api/sms/send
Send an SMS message.

**Request Body:**
```json
{
  "phoneNumber": "+1987654321",
  "message": "Your appointment is confirmed for tomorrow at 2 PM."
}
```

## 📧 Telegram Endpoints

#### GET /api/telegram/conversations
Get Telegram conversations.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "contactName": "Charlie Brown",
      "username": "@charlie_brown",
      "lastMessage": "Thanks for the quick response!",
      "timestamp": "2025-01-23T15:20:00Z",
      "unreadCount": 0,
      "status": "active"
    }
  ]
}
```

## 📅 Appointments Endpoints

#### GET /api/appointments
Get appointments.

**Query Parameters:**
- `date` (optional): Filter by date (YYYY-MM-DD)
- `status` (optional): Filter by status (`confirmed`, `pending`, `cancelled`, `completed`)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patientName": "John Doe",
      "phoneNumber": "+1234567890",
      "appointmentDate": "2025-01-24",
      "appointmentTime": "14:00",
      "status": "confirmed",
      "service": "Consultation",
      "notes": "First visit"
    }
  ]
}
```

#### POST /api/appointments
Create a new appointment.

**Request Body:**
```json
{
  "patientName": "John Doe",
  "phoneNumber": "+1234567890",
  "appointmentDate": "2025-01-24",
  "appointmentTime": "14:00",
  "service": "Consultation",
  "notes": "First visit"
}
```

#### PUT /api/appointments/{id}
Update appointment.

**Request Body:**
```json
{
  "status": "confirmed",
  "notes": "Patient confirmed attendance"
}
```

#### DELETE /api/appointments/{id}
Cancel appointment.

**Response:**
```json
{
  "success": true,
  "message": "Appointment cancelled successfully"
}
```

## 📞 Outbound Calls Endpoints

#### GET /api/outbound-calls
Get outbound call campaigns.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "campaignName": "Appointment Reminders",
      "status": "active",
      "totalCalls": 150,
      "completedCalls": 120,
      "successRate": 80.0,
      "createdAt": "2025-01-23T09:00:00Z"
    }
  ]
}
```

#### POST /api/outbound-calls
Create outbound call campaign.

**Request Body:**
```json
{
  "campaignName": "Follow-up Calls",
  "phoneNumbers": ["+1234567890", "+1987654321"],
  "message": "This is a follow-up call regarding your recent visit.",
  "scheduledTime": "2025-01-24T10:00:00Z"
}
```

## ⚙️ System Endpoints

#### GET /api/system/status
Get system status and health.

**Response:**
```json
{
  "success": true,
  "data": {
    "whatsappApi": "online",
    "callSystem": "online",
    "database": "online",
    "lastUpdated": "2025-01-23T16:00:00Z",
    "uptime": "2 days, 14 hours, 32 minutes"
  }
}
```

#### GET /api/system/activity
Get recent system activity.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "type": "outbound_call",
      "description": "Outbound call completed to +1234567890",
      "timestamp": "2025-01-23T15:45:00Z",
      "status": "success"
    },
    {
      "id": 2,
      "type": "whatsapp_message",
      "description": "WhatsApp message from John Doe",
      "timestamp": "2025-01-23T15:30:00Z",
      "status": "received"
    }
  ]
}
```

## 🔧 Configuration Endpoints

#### GET /api/config/whatsapp
Get WhatsApp configuration.

**Response:**
```json
{
  "success": true,
  "data": {
    "apiUrl": "https://api.whatsapp.com",
    "webhookUrl": "https://yourdomain.com/webhook/whatsapp",
    "status": "connected",
    "lastSync": "2025-01-23T16:00:00Z"
  }
}
```

#### PUT /api/config/whatsapp
Update WhatsApp configuration.

**Request Body:**
```json
{
  "apiToken": "your-whatsapp-api-token",
  "webhookUrl": "https://yourdomain.com/webhook/whatsapp"
}
```

## 📊 Analytics Endpoints

#### GET /api/analytics/overview
Get analytics overview.

**Query Parameters:**
- `period`: `today`, `week`, `month`, `year`

**Response:**
```json
{
  "success": true,
  "data": {
    "totalCalls": 1250,
    "totalMessages": 3400,
    "totalAppointments": 450,
    "averageResponseTime": "2.5 minutes",
    "customerSatisfaction": 4.2
  }
}
```

## 🚨 Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "phoneNumber",
      "issue": "Invalid phone number format"
    }
  }
}
```

### Common Error Codes
- `AUTHENTICATION_REQUIRED`: Missing or invalid token
- `AUTHORIZATION_FAILED`: Insufficient permissions
- `VALIDATION_ERROR`: Invalid input data
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

## 📡 WebSocket Events

The application supports real-time updates via WebSocket connections.

### Connection
```javascript
const socket = io('https://60h5imcyqzzl.manus.space');
```

### Events

#### Incoming Messages
- `new_whatsapp_message`: New WhatsApp message received
- `new_sms_message`: New SMS message received
- `new_telegram_message`: New Telegram message received
- `call_status_update`: Call status changed
- `appointment_update`: Appointment status changed

#### Outgoing Events
- `join_room`: Join specific room for updates
- `leave_room`: Leave room
- `mark_as_read`: Mark messages as read

### Example Usage
```javascript
// Listen for new WhatsApp messages
socket.on('new_whatsapp_message', (data) => {
  console.log('New message:', data);
  // Update UI
});

// Join conversation room
socket.emit('join_room', { room: 'whatsapp_conversation_1' });
```

## 🔄 Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Message endpoints**: 100 requests per hour
- **General endpoints**: 1000 requests per hour

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642780800
```

## 📝 Request/Response Examples

### cURL Examples

#### Login
```bash
curl -X POST https://60h5imcyqzzl.manus.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "clinicName": "Test Clinic",
    "username": "demo",
    "password": "demo"
  }'
```

#### Get Dashboard Stats
```bash
curl -X GET https://60h5imcyqzzl.manus.space/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Send WhatsApp Message
```bash
curl -X POST https://60h5imcyqzzl.manus.space/api/whatsapp/conversations/1/messages \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How can I help you today?",
    "type": "text"
  }'
```

---

**API Version**: 2.1.0  
**Last Updated**: January 2025  
**Base URL**: https://60h5imcyqzzl.manus.space


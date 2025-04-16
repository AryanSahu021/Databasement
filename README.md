# SafeDocs – Secure File Management System

**Group Name:** Databasement  
**GitHub Repository:** [Databasement](https://github.com/AryanSahu021/Databasement)  
**Demo Video:** [Watch Demo](https://youtu.be/NWklnray_2Q)

---

##  Objective

SafeDocs is a secure file management system that enables authenticated members to upload, manage, and share files within a group. It integrates with the **centralized CIMS database** to provide:

- Secure authentication and session validation  
- Role-based access control  
- Audit trails for critical actions  
- Seamless integration with member data from the central system

---

##  Database Design

### Group-Specific Tables (in `cs432g12`)

| Table Name        | Description                          | Fields                                                                 |
|-------------------|--------------------------------------|------------------------------------------------------------------------|
| `pdfdocument`     | Stores file metadata                 | DocumentID, OwnerID, FilePath, UploadTimestamp                         |
| `folder`          | Represents user folders              | FolderID, MemberID, FolderName, FolderType                             |
| `folderdocuments` | Maps files to folders                | FolderID, DocumentID                                                   |
| `accesscontrol`   | Manages access rights                | DocumentID, MemberID, AccessLevel (view/edit)                          |
| `sharedrequests`  | Pending access requests              | RequestID, SenderID, ReceiverID, DocumentID, Status                    |

 All tables are created using SQL scripts and avoid duplicating centralized data.

---

## CIMS Integration

### Dual Database Access
- `get_connection()` → connects to **cs432cims** (central)
- `get_connection(0)` → connects to **cs432g12** (group)

### Shared Central Tables (Read-Only):
- `members`
- `login`
- `membergroupmapping`

### Cross-Database Member Deletion:
- Checks member existence in other groups  
- Deletes from `members` and `login` only if no other group references  
- Always removes from `membergroupmapping` for the group

---

## Session & Access Control

### Session Middleware
- `@is_valid_session` used on protected routes  
- Validates session via: `http://10.0.116.125:5000/isValidSession`

### Access Control
- **Admin:** Full access – edit users, create admins, delete members  
- **Regular User:** Can only manage personal files and requests

### Frontend Security
- Confirmation modals for delete operations  
- UI elements shown based on session role

---

## API Endpoints

| Action               | Method | Endpoint                               | Access         | Description                           |
|----------------------|--------|----------------------------------------|----------------|---------------------------------------|
| Login                | POST   | `/login`                               | Public         | Authenticates using central API       |
| Logout               | GET    | `/logout`                              | Authenticated  | Ends session                          |
| Upload File          | POST   | `/upload`                              | Authenticated  | Uploads file and stores metadata      |
| View File            | GET    | `/files/<token>`                       | AccessControlled| Opens file if access is granted       |
| Delete File          | DELETE | `/files/<doc_id>`                      | Owner/Admin    | Deletes file                          |
| Send Share Request   | POST   | `/shared_requests/send`               | Authenticated  | Sends a file access request           |
| Update Share Request | POST   | `/shared_requests/<id>/update`        | Receiver       | Accepts/rejects access request        |
| View Portfolio       | GET    | `/portfolio`                           | Authenticated  | Displays group members                |
| Edit Portfolio       | POST   | `/portfolio/edit`                      | Admin          | Edits member data                     |

---

## Logging & Audit Trail

### Tracked Actions:
- File uploads/deletions  
- Access requests  
- Member edits and deletions

### How It Works:
- Logs written to `auditlog` table with:  
  `MemberID`, `ActionType`, `DocumentID`, `Timestamp`  
- Unauthorized attempts logged via session validation failures

---

## Member Management

### Portfolio
- Displays all group members (from `membergroupmapping`)  
- Admins can update roles/emails  
- Regular users can view their profile only

### Member Creation
- By user (self-register) or by admin  
- Password hashed before DB insert  
- Uses centralized login system for token-based auth

### Member Deletion
- Checks group membership  
- Deletes from `members` and `login` only if no other group is associated  
- Logs action in `auditlog` and server logs

---

## 🧑‍💻 Team Members and Contributions

| Name          | Roll No.   | Contributions                                                             |
|---------------|------------|----------------------------------------------------------------------------|
| Aryan Sahu    | 22110038   | Flask backend, API integration, CIMS DB access, Session handling, Folders |
| Dewansh Kumar | 22110071   | Frontend (HTML/CSS/JS), Modals, Role-based UI, SQL scripts, Audit logs    |

---

## 🎥 Demo Video

📽️ [Watch Here](https://youtu.be/NWklnray_2Q)  
**Covers:**
- Login and session validation  
- File upload and folder creation  
- Sharing requests and access control  
- Admin privileges and logs

---

## **Appendix**

- **SQL Admin**: [http://10.0.116.125/phpmyadmin](http://10.0.116.125/phpmyadmin)  
- **Auth Server**: [http://10.0.116.125:5000](http://10.0.116.125:5000)  
- **Group DB**: `cs432g9`  
- **Central DB**: `cs432cims`

---

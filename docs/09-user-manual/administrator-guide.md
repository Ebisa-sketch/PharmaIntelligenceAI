# System Administrator Guide

## PharmaIntelligence AI — Administration Manual

> **Document status:** Draft  
> **Last updated:** 2026-11-05

---

## 1. Overview

This guide is for **System Administrators** responsible for managing the PharmaIntelligence AI platform, including user accounts, facility configuration, system settings, and audit oversight.

---

## 2. Initial System Setup

### 2.1 First login

After deployment, an initial administrator account is created via the database seed script. Use these credentials to log in and immediately change the default password.

### 2.2 System configuration

Navigate to **Settings** to configure:

- Application name and branding
- Default data import formats
- Session timeout duration
- Password policy (minimum length, complexity)
- API rate limits

---

## 3. User Management

### 3.1 Creating user accounts

1. Navigate to **Users** in the sidebar
2. Click **Add User**
3. Enter email, name, and assign one or more roles
4. The user receives a temporary password or invitation link

### 3.2 Available roles

| Role | Access Level |
|------|-------------|
| System Administrator | Full system access, user management, configuration |
| Facility Pharmacy Manager | Facility-scoped inventory, forecasts, risk views |
| Regional Supply Chain Manager | Multi-facility aggregated views, redistribution approval |
| Data Analyst / Researcher | Data import, quality assessment, model experiments |
| Auditor | Read-only access to audit logs, decisions, approvals |

### 3.3 Deactivating accounts

Deactivated accounts cannot log in but their audit history is preserved. Navigate to the user profile and toggle **Active** status.

---

## 4. Facility Management

### 4.1 Registering facilities

1. Navigate to **Facilities**
2. Click **Add Facility**
3. Enter facility ID, name, type (hospital, health centre), region, and location
4. Assign users who have access to this facility's data

### 4.2 Facility data isolation

Each facility's inventory, predictions, and recommendations are isolated. A user can only see facilities they are explicitly assigned to, unless they hold a regional or administrator role.

---

## 5. Data Import Administration

### 5.1 Import permissions

Only users with the Data Analyst or Administrator role can perform data imports.

### 5.2 Monitoring imports

Navigate to **Audit Logs** → filter by **Import** events to review:

- Who imported which file and when
- Row counts (accepted, rejected, duplicates)
- Validation errors

### 5.3 Preventing duplicate imports

The system checks file hashes and record signatures to prevent silent duplication. Re-importing the same file will prompt a warning.

---

## 6. Audit Logs

### 6.1 What is logged

- User authentication events (login, logout, failed attempts)
- Administrative changes (user creation, role changes, facility assignments)
- Data imports and validation results
- Redistribution recommendation reviews and approvals
- System configuration changes

### 6.2 Reviewing logs

Navigate to **Audit Logs** and filter by:

- Date range
- User
- Action type
- Facility

### 6.3 Log protection

Audit records are append-only and cannot be modified or deleted through the application interface.

---

## 7. Backup and Recovery

- Coordinate with DevOps for database backup schedules
- Verify backup integrity monthly
- Document the restore procedure and test it in a staging environment

---

## 8. Security Responsibilities

- Enforce strong password policies
- Review user access quarterly and remove stale accounts
- Monitor failed login attempts for potential unauthorized access
- Ensure secrets and API keys are rotated periodically
- Report any suspected data breach immediately


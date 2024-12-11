--Drop the table if it already exists
DROP TABLE IF EXISTS UserProfiles;
DROP TABLE IF EXISTS Emails;
DROP TABLE IF EXISTS EmailResponses;
DROP TABLE IF EXISTS UserTrainingRecommendations;

--Create the UserProfiles table
CREATE TABLE UserProfiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    department TEXT,
    role TEXT,
    training_status TEXT
);

--Create the Emails table
CREATE TABLE Emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    recipients TEXT,
    subject TEXT,
    body TEXT,
    timestamp TEXT,
    attachments TEXT
);

CREATE TABLE SourceEmails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    sender TEXT NOT NULL,
    subject TEXT,
    body TEXT,
    timestamp TEXT,
    attachments TEXT
);

--Create the EmailResponses table
CREATE TABLE EmailResponses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id INTEGER,
    user_email TEXT,
    response_type TEXT,
    timestamp TEXT,
    FOREIGN KEY (email_id) REFERENCES Emails(id)
);

--Create the UserTrainingRecommendations table
CREATE TABLE UserTrainingRecommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    recommended_module TEXT,
    status TEXT
);

--Insert sample data into UserProfiles
INSERT INTO UserProfiles (email, department, role, training_status)
VALUES
    ('john.doe@company.com', 'HR', 'Manager', 'Completed'),
    ('jane.smith@company.com', 'IT', 'Developer', 'In Progress'),
    ('mary.jones@company.com', 'Finance', 'Accountant', 'Not Started'),
    ('lucas.brown@company.com', 'HR', 'Assistant', 'Completed'),
    ('emily.davis@company.com', 'Marketing', 'Lead', 'In Progress'),
    ('william.king@company.com', 'IT', 'SysAdmin', 'Completed'),
    ('olivia.martin@company.com', 'Sales', 'Sales Manager', 'Not Started'),
    ('emma.white@company.com', 'Marketing', 'Coordinator', 'In Progress');

--Insert sample data into Emails
INSERT INTO Emails (sender, recipients, subject, body, timestamp, attachments)
VALUES 
    ('security@company.com', 'john.doe@company.com', 'Phishing Alert: Urgent Update', 'Please click the link to verify your account.', '2024-12-01 08:30:00', NULL),
    ('hr@company.com', 'mary.jones@company.com', 'Company Update: New Policies', 'Click here to review new policies.', '2024-12-02 09:15:00', NULL),
    ('admin@company.com', 'lucas.brown@company.com', 'Monthly Report', 'Here is your report for this month.', '2024-12-03 10:00:00', 'report.pdf'),
    ('sales@company.com', 'emily.davis@company.com', '50% Off: Special Promotion', 'Hurry, the sale ends soon!', '2024-12-04 11:45:00', NULL),
    ('helpdesk@company.com', 'jane.smith@company.com', 'Security Alert: Suspicious Activity', 'Your account may have been compromised.', '2024-12-05 12:30:00', NULL),
    ('marketing@company.com', 'william.king@company.com', 'New Campaign Launch', 'Check out our latest campaign!', '2024-12-06 14:00:00', 'campaign_image.jpg'),
    ('finance@company.com', 'olivia.martin@company.com', 'Quarterly Financial Report', 'Review the attached financial report for Q4.', '2024-12-07 16:30:00', 'Q4_financials.pdf'),
    ('hr@company.com', 'emma.white@company.com', 'Workshops on Leadership', 'Join us for a series of leadership workshops.', '2024-12-08 17:00:00', NULL);


INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('john.doe@company.com', 'security@company.com', 'Phishing Alert: Urgent Update', 'Please click the link to verify your account.', '2024-12-01 08:30:00', NULL),
    ('john.doe@company.com', 'hr@company.com', 'Company Update: New Policies', 'Click here to review new policies.', '2024-12-02 09:15:00', NULL),
    ('john.doe@company.com', 'admin@company.com', 'Monthly Report', 'Here is your report for this month.', '2024-12-03 10:00:00', 'report.pdf'),
    ('mary.jones@company.com', 'hr@company.com', 'Company Update: New Policies', 'Click here to review new policies.', '2024-12-02 09:15:00', NULL),
    ('lucas.brown@company.com', 'admin@company.com', 'Monthly Report', 'Here is your report for this month.', '2024-12-03 10:00:00', 'report.pdf'),
    ('emily.davis@company.com', 'sales@company.com', '50% Off: Special Promotion', 'Hurry, the sale ends soon!', '2024-12-04 11:45:00', NULL),
    ('jane.smith@company.com', 'helpdesk@company.com', 'Security Alert: Suspicious Activity', 'Your account may have been compromised.', '2024-12-05 12:30:00', NULL),
    ('william.king@company.com', 'marketing@company.com', 'New Campaign Launch', 'Check out our latest campaign!', '2024-12-06 14:00:00', 'campaign_image.jpg'),
    ('olivia.martin@company.com', 'finance@company.com', 'Quarterly Financial Report', 'Review the attached financial report for Q4.', '2024-12-07 16:30:00', 'Q4_financials.pdf'),
    ('emma.white@company.com', 'hr@company.com', 'Workshops on Leadership', 'Join us for a series of leadership workshops.', '2024-12-08 17:00:00', NULL);

--Insert sample data into EmailResponses
INSERT INTO EmailResponses (email_id, user_email, response_type, timestamp)
VALUES
    (1, 'john.doe@company.com', 'Clicked', '2024-12-01 08:35:00'),
    (2, 'mary.jones@company.com', 'Ignored', '2024-12-02 09:20:00'),
    (3, 'lucas.brown@company.com', 'Opened', '2024-12-03 10:05:00'),
    (4, 'emily.davis@company.com', 'Clicked', '2024-12-04 11:50:00'),
    (5, 'jane.smith@company.com', 'Ignored', '2024-12-05 12:35:00'),
    (6, 'william.king@company.com', 'Opened', '2024-12-06 14:05:00'),
    (7, 'olivia.martin@company.com', 'Clicked', '2024-12-07 16:35:00'),
    (8, 'emma.white@company.com', 'Ignored', '2024-12-08 17:10:00');

--Insert sample data into UserTrainingRecommendations
INSERT INTO UserTrainingRecommendations (user_email, recommended_module, status)
VALUES
    ('john.doe@company.com', 'Phishing Awareness', 'Completed'),
    ('jane.smith@company.com', 'Advanced Phishing Tactics', 'In Progress'),
    ('mary.jones@company.com', 'Phishing Awareness', 'Not Started'),
    ('lucas.brown@company.com', 'Email Security', 'Completed'),
    ('emily.davis@company.com', 'Phishing Awareness', 'In Progress'),
    ('william.king@company.com', 'System Security Basics', 'Completed'),
    ('olivia.martin@company.com', 'Advanced Phishing Tactics', 'Not Started'),
    ('emma.white@company.com', 'Email Security', 'In Progress');


--Additional emails for John Doe (HR Manager)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('john.doe@company.com', 'hr@company.com', 'Annual HR Survey', 'Please complete the annual HR survey.', '2024-12-09 08:00:00', NULL),
    ('john.doe@company.com', 'admin@company.com', 'Employee Benefits Update', 'Review the updated employee benefits for 2025.', '2024-12-10 09:00:00', NULL),
    ('john.doe@company.com', 'helpdesk@company.com', 'System Maintenance Notification', 'System maintenance will occur this weekend.', '2024-12-11 10:30:00', NULL),
    ('john.doe@company.com', 'marketing@company.com', 'HR Campaign: Employee Wellness', 'Join us for a wellness campaign starting this month.', '2024-12-12 11:45:00', NULL);

--Additional emails for Mary Jones (Finance Accountant)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('mary.jones@company.com', 'finance@company.com', 'End-of-Year Financial Overview', 'Please review the attached financial overview for the year.', '2024-12-09 09:00:00', 'overview.pdf'),
    ('mary.jones@company.com', 'hr@company.com', 'Employee Bonus Announcement', 'We are happy to announce the employee bonuses for 2024.', '2024-12-10 10:15:00', NULL),
    ('mary.jones@company.com', 'admin@company.com', 'Tax Filing Deadline', 'Reminder: The tax filing deadline is approaching.', '2024-12-11 11:00:00', NULL),
    ('mary.jones@company.com', 'sales@company.com', 'Sales Incentive Report', 'Here is the latest sales incentive report for Q4.', '2024-12-12 12:30:00', NULL);

--Additional emails for Lucas Brown (HR Assistant)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('lucas.brown@company.com', 'hr@company.com', 'Employee Recognition Event', 'You are invited to the employee recognition event.', '2024-12-09 08:30:00', NULL),
    ('lucas.brown@company.com', 'marketing@company.com', 'Internal Newsletter: HR Section', 'Please review the HR section for the upcoming internal newsletter.', '2024-12-10 09:45:00', NULL),
    ('lucas.brown@company.com', 'helpdesk@company.com', 'Employee Profile Update', 'Please ensure your profile information is up-to-date.', '2024-12-11 10:00:00', NULL),
    ('lucas.brown@company.com', 'finance@company.com', 'Payroll Update', 'The payroll for this month has been updated.', '2024-12-12 11:00:00', NULL);

--Additional emails for Emily Davis (Marketing Lead)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('emily.davis@company.com', 'marketing@company.com', 'New Marketing Campaign Launch', 'Exciting new campaign launching next week. Stay tuned!', '2024-12-09 10:00:00', NULL),
    ('emily.davis@company.com', 'sales@company.com', 'Sales Strategy Meeting', 'We are meeting to discuss the new sales strategy.', '2024-12-10 11:15:00', NULL),
    ('emily.davis@company.com', 'hr@company.com', 'Marketing Team Training Session', 'Join us for a training session on new marketing tools.', '2024-12-11 12:00:00', NULL),
    ('emily.davis@company.com', 'admin@company.com', 'Office Decor Update', 'The office decor will be updated next week. Please review.', '2024-12-12 13:30:00', NULL);

--Additional emails for William King (IT SysAdmin)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('william.king@company.com', 'it@company.com', 'System Update Notification', 'A system update is scheduled for this weekend.', '2024-12-09 12:30:00', NULL),
    ('william.king@company.com', 'marketing@company.com', 'Tech Tools for Marketing Team', 'Check out the new tools that will support the marketing team.', '2024-12-10 13:45:00', NULL),
    ('william.king@company.com', 'admin@company.com', 'Network Maintenance Schedule', 'We will be performing network maintenance on Friday.', '2024-12-11 14:00:00', NULL),
    ('william.king@company.com', 'hr@company.com', 'Employee Tech Support Needs', 'Please review the list of employee tech support requests.', '2024-12-12 15:00:00', NULL);

--Additional emails for Olivia Martin (Sales Manager)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('olivia.martin@company.com', 'sales@company.com', 'New Sales Target Set', 'We have set new sales targets for Q1. Please review.', '2024-12-09 09:30:00', NULL),
    ('olivia.martin@company.com', 'finance@company.com', 'Quarterly Sales Review', 'Please review the quarterly sales review document.', '2024-12-10 10:45:00', 'sales_review.pdf'),
    ('olivia.martin@company.com', 'marketing@company.com', 'Product Launch Support', 'Marketing is offering support for the new product launch.', '2024-12-11 11:30:00', NULL),
    ('olivia.martin@company.com', 'helpdesk@company.com', 'Sales Team IT Support', 'The sales team requires additional IT support for presentations.', '2024-12-12 12:00:00', NULL);

--Additional emails for Emma White (Marketing Coordinator)
INSERT INTO SourceEmails (user_email, sender, subject, body, timestamp, attachments)
VALUES
    ('emma.white@company.com', 'marketing@company.com', 'Marketing Strategy for 2025', 'Let’s discuss the marketing strategy for the next year.', '2024-12-09 08:15:00', NULL),
    ('emma.white@company.com', 'sales@company.com', 'Upcoming Product Launch Events', 'Join us for the product launch event planning meeting.', '2024-12-10 09:30:00', NULL),
    ('emma.white@company.com', 'hr@company.com', 'Employee Engagement Survey Results', 'Please review the results of the recent engagement survey.', '2024-12-11 10:30:00', NULL),
    ('emma.white@company.com', 'admin@company.com', 'Holiday Party Planning', 'We are planning a holiday party. Here are the details.', '2024-12-12 11:00:00', NULL);

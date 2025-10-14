INSERT INTO organizations (org_id, org_name) VALUES
(1, 'Org1'),
(2, 'Org2');

INSERT INTO interview_templates (template_id, org_id, template_name) VALUES
(101, 1, 'Backend Developer Template'),
(102, 2, 'Data Scientist Template');

INSERT INTO questions (question_id, template_id, question_text, expected_answer, weightage, question_order) VALUES
-- For Backend Developer Template
(1001, 101, 'How willing are you to travel between Germany and Switzerland every week?', 'Weekly mobility is mandatory.', 20.00, 1),
(1002, 101, 'What kind of working and communication culture brings out your best performance?', 'Cultural fit sustains team performance.', 15.00, 2),
(1003, 101, 'Describe a time when feedback fundamentally changed how you worked.', 'Tests openness & learning agility.', 10.00, 3),
(1004, 101, 'How do you react when priorities shift suddenly and information is incomplete?', 'Measures comfort with ambiguity.', 10.00, 4),
(1005, 101, 'Which personal values are non-negotiable for you, and how do they show up at work?', 'Values alignment.', 10.00, 5),
(1006, 101, 'Tell me about a team conflict you resolved—what was your specific contribution?', 'Conflict-resolution skills.', 10.00, 6),
(1007, 101, 'What motivates you to stay committed in this role long-term?', 'Checks sustained drive.', 10.00, 7),
(1008, 101, 'How do you keep your technical and personal skills up to date?', 'Continuous self-development.', 10.00, 8),
(1009, 101, 'What conditions (time, place, tools) do you need to deliver peak performance?', 'Compatibility with work models.', 5.00, 9),
(1010, 101, 'Is there anything that could limit your performance in this job that we should know?', 'Early detection of red flags.', 5.00, 10),

-- For Data Scientist Template
(1011, 102, 'What is overfitting?', 'Model fits noise instead of pattern', 10.00, 1),
(1012, 102, 'Define precision and recall.', 'Classification performance metrics', 15.00, 2),
(1013, 102, 'Explain cross-validation.', 'Model evaluation technique', 20.00, 3);

INSERT INTO candidates (candidate_id, full_name, email, org_id) VALUES
(201, 'John Doe', 'john.doe@example.com', 1),
(202, 'Jane Smith', 'jane.smith@example.com', 2);

INSERT INTO interviews (interview_id, candidate_id, template_id, status, total_score, transcript_file_path) VALUES
(301, 201, 102, 'scored', 42.50, '/transcripts/john_doe.txt'),
(302, 202, 101, 'pending', NULL, NULL);

-- Insert candidate answers
INSERT INTO candidate_answers (answer_id, interview_id, question_id, response_text, score, ai_comments) VALUES
('1', '301', '1001', 'So I''m fully comfortable with Monday to Thursday rhythm in Zurich and Fridays I''m back in Berlin. So I have done that for 2 years already and this kind of logistics is no problem for me and it''s a second nature, so I can easily deal with that. ', 0.0, NULL),
('2', '301', '1002', 'Yeah, fully driven teams, , that practice radical transparency, so open dashboards, short, short feedback loops, and decision making that''s biased to action when everyone can speak up and data is shared in real time, I do my best work. ', 0.0, NULL),
('3', '301', '1003', 'Yeah, during a code review, our CTO pointed out that my modules lacked test coverage, which slowed slowed  onboarding. So I re-engineered my workflow to write tests first and peer review documentation. Six months later, our onboarding time dropped by 40%. ', 0.0, NULL),
('4', '301', '1004', 'Yeah, I''m that guy. I sketch a quick impact matrix for myself always and align on the good enough decision, then deliver an MVP within 24 hours. That''s mainly when I do it, what I do in such kind of situation and  that creates learning data and lets us  course correct without over engineering.', 0.0, NULL),
('5', '301', '1005', 'Oh wow, yeah, so integrity and ownership if I commit, I deliver no hidden blockers. I try to escalate and risk early then surprise the team later so that''s really a personal value that is nonnegotiation for me. ', 0.0, NULL),
('6', '301', '1006', 'Yeah, so once two engineers were talking debating a code style, I scheduled the 5 15 minute peer review session, facilitated the conversation, and we agreed on a for a matter that both adopted. Tension dissolved and velocity rebounded the next sprint. ', 0.0, NULL),
('7', '301', '1007', 'The chance to scale a cross-border web tree product aligns perfectly with my career path. Building trust in decentralized tech between Germany and Switzerland markets is a mission I can wake up really excited  about about for years. ', 0.0, NULL),
('8', '301', '1008', 'Yeah, I upskilled myself all the time, so I''m I really know which skills are very fundamental to me and I have newsletter that I read. I have some peers group where we talk  all the time about . About the new upcoming technologies and  so this is how I upskill myself. It''s mainly I don''t do a full degree like of advanced studies, but I really focus on on all the news and if there is something very new I really dig deep into that. , that''s how I. Keep it up to date. ', 0.0, NULL),
('9', '301', '1009', 'I need a quiet workplace, and the best hours for me are from 100 a.m. to 4 p.m. central European time. And  I really like to have a communication tool where I get fast feedback from all the developers . Something like slack, for example. But this is mainly how, how I work very great and can make peak performance. And I always I also think when we when I write to to all the . Employees or other are writing to me that we expect from each other that we write back within the next 24 hours so that  that I can know, OK, I can let that . I can let that be for some time and can really focus on. On, on, on working on my. My Yeah, my delivers without getting distracted all the time. ', 0.0, NULL),
('10', '301', '1010', 'So there''s nothing on the horizon. My resident permits cover Switzerland and my health is solid and my family fully supports the travel schedule, so should be everything fine.', 0.0, NULL)














 
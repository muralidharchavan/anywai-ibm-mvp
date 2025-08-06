CREATE TABLE organizations (
    org_id INT PRIMARY KEY,
    org_name TEXT NOT NULL
);

CREATE TABLE interview_templates (
    template_id INT PRIMARY KEY,
    org_id INT REFERENCES organizations(org_id),
    template_name TEXT NOT NULL
);

CREATE TABLE questions (
    question_id INT PRIMARY KEY,
    template_id INT REFERENCES interview_templates(template_id),
    question_text TEXT NOT NULL,
    expected_answer TEXT,
    weightage NUMERIC(5,2),
    question_order INT
);

CREATE TABLE candidates (
    candidate_id INT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    org_id INT REFERENCES organizations(org_id)
);

CREATE TABLE interviews (
    interview_id INT PRIMARY KEY,
    candidate_id INT REFERENCES candidates(candidate_id),
    template_id INT REFERENCES interview_templates(template_id),
    status TEXT CHECK (status IN ('pending', 'processing', 'scored', 'error')),
    total_score NUMERIC(5,2),
    transcript_file_path TEXT
);

CREATE TABLE candidate_answers (
    answer_id INT PRIMARY KEY,
    interview_id INT REFERENCES interviews(interview_id),
    question_id INT REFERENCES questions(question_id),
    ans_vid_filename TEXT,
    response_text TEXT,
    score NUMERIC(5,2),
    ai_comments TEXT
);

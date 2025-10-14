-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.candidate_answers (
  answer_id integer NOT NULL,
  interview_id integer,
  question_id integer,
  response_text text,
  score numeric,
  ai_comments text,
  ans_vid_filename text,
  CONSTRAINT candidate_answers_pkey PRIMARY KEY (answer_id),
  CONSTRAINT candidate_answers_interview_id_fkey FOREIGN KEY (interview_id) REFERENCES public.interviews(interview_id),
  CONSTRAINT candidate_answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(question_id)
);
CREATE TABLE public.candidates (
  candidate_id integer NOT NULL,
  full_name text NOT NULL,
  email text,
  org_id integer,
  CONSTRAINT candidates_pkey PRIMARY KEY (candidate_id),
  CONSTRAINT candidates_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(org_id)
);
CREATE TABLE public.interview_templates (
  template_id integer NOT NULL,
  org_id integer,
  template_name text NOT NULL,
  CONSTRAINT interview_templates_pkey PRIMARY KEY (template_id),
  CONSTRAINT interview_templates_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(org_id)
);
CREATE TABLE public.interviews (
  interview_id integer NOT NULL,
  candidate_id integer,
  template_id integer,
  status text CHECK (status = ANY (ARRAY['pending'::text, 'processing'::text, 'scored'::text, 'error'::text])),
  total_score numeric,
  transcript_file_path text,
  CONSTRAINT interviews_pkey PRIMARY KEY (interview_id),
  CONSTRAINT interviews_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id),
  CONSTRAINT interviews_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.interview_templates(template_id)
);
CREATE TABLE public.organizations (
  org_id integer NOT NULL,
  org_name text NOT NULL,
  CONSTRAINT organizations_pkey PRIMARY KEY (org_id)
);
CREATE TABLE public.questions (
  question_id integer NOT NULL,
  template_id integer,
  question_text text NOT NULL,
  expected_answer text,
  weightage numeric,
  question_order integer,
  CONSTRAINT questions_pkey PRIMARY KEY (question_id),
  CONSTRAINT questions_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.interview_templates(template_id)
);
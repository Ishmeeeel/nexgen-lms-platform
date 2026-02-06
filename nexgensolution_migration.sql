-- NexGenSolution LMS FULL Migration Script
-- (Tables + RLS + Teacher + Admin Policies)

-- 0) Safety
create extension if not exists pgcrypto;

-- 1) Tables
CREATE TABLE IF NOT EXISTS profiles (...);
CREATE TABLE IF NOT EXISTS courses (...);
CREATE TABLE IF NOT EXISTS lessons (...);
CREATE TABLE IF NOT EXISTS enrollments (...);
CREATE TABLE IF NOT EXISTS submissions (...);
CREATE TABLE IF NOT EXISTS grades (...);
CREATE TABLE IF NOT EXISTS events (...);
CREATE TABLE IF NOT EXISTS instructors (...);

-- 2) Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE instructors ENABLE ROW LEVEL SECURITY;

-- 3) Student policies
CREATE POLICY ...
CREATE POLICY ...
etc...

-- 4) Teacher policies
CREATE POLICY ...
etc...

-- 5) Admin policies
CREATE POLICY ...
etc...

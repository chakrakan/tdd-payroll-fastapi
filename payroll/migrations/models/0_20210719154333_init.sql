-- upgrade --
CREATE TABLE IF NOT EXISTS "job_group" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "group" VARCHAR(1) NOT NULL  PRIMARY KEY,
    "hourly_rate" DECIMAL(8,2) NOT NULL,
    CONSTRAINT "uid_job_group_group_5db1ae" UNIQUE ("group", "hourly_rate")
);
COMMENT ON TABLE "job_group" IS 'JobGroup model for the DB';
CREATE TABLE IF NOT EXISTS "employee" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "job_group_id" VARCHAR(1) NOT NULL REFERENCES "job_group" ("group") ON DELETE CASCADE
);
COMMENT ON TABLE "employee" IS 'An extensible class to manage Employees in the DB';
CREATE TABLE IF NOT EXISTS "employee_report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "start_date" TIMESTAMPTZ NOT NULL,
    "end_date" TIMESTAMPTZ NOT NULL,
    "amount_paid" DECIMAL(14,2) NOT NULL,
    "report_employee_id" INT NOT NULL REFERENCES "employee" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "employee_report" IS 'More Specific EmployeeReport class to generate report structure from';
CREATE TABLE IF NOT EXISTS "time_report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "report_id" INT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL,
    "hours_worked" DECIMAL(4,2) NOT NULL,
    "employee_id" INT NOT NULL REFERENCES "employee" ("id") ON DELETE CASCADE,
    "job_group_id" VARCHAR(1) NOT NULL REFERENCES "job_group" ("group") ON DELETE CASCADE
);
COMMENT ON TABLE "time_report" IS 'Time Report class to contain parsed CSV info... pretty much a data dump';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

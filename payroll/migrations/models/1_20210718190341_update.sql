-- upgrade --
ALTER TABLE "time_report" ALTER COLUMN "date" TYPE TIMESTAMPTZ USING "date"::TIMESTAMPTZ;
-- downgrade --
ALTER TABLE "time_report" ALTER COLUMN "date" TYPE DATE USING "date"::DATE;

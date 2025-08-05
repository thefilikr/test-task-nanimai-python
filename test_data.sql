-- USERS
INSERT INTO users (id, email, created_at) VALUES
  ('11111111-1111-1111-1111-111111111111', 'user1@example.com', NOW()),
  ('22222222-2222-2222-2222-222222222222', 'user2@example.com', NOW());

-- BALANCES
INSERT INTO balances (id, user_id, amount, limit, updated_at) VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 1000.00, 2000.00, NOW()),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-2222-2222-2222-222222222222', 500.00, 1000.00, NOW());

-- TRANSACTIONS
-- INSERT INTO transactions (id, user_id, amount, status, operation_type, created_at)
-- VALUES
--   ('cccccccc-cccc-cccc-cccc-cccccccccccc', '11111111-1111-1111-1111-111111111111', 100.00, 'pending', 'reserve', NOW()),
--   ('dddddddd-dddd-dddd-dddd-dddddddddddd', '11111111-1111-1111-1111-111111111111', 200.00, 'confirmed', 'reserve', NOW()),
--   ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '22222222-2222-2222-2222-222222222222', 50.00, 'canceled', 'reserve', NOW());
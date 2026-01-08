INSERT INTO public.financeiro_contas (id, id_origem, agencia, conta, digito_verificador, descricao, data_criacao, tenant_id, instituicao_financeira_id) VALUES
-- Para Banco Alfa (tenant 01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101)
('5a1fbbcb-4eeb-42d9-bca8-7a1813b441c3', 'origem-1', '001', '12345-6', '7', 'Conta 1 do Banco Alfa', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101', 'c9f2b8d2-7a2b-4a0e-b7bc-0e1b34407dcb'),
('d97f12d8-f39c-4a23-8f3b-926e3c4775ec', 'origem-2', '001', '12346-7', '8', 'Conta 2 do Banco Alfa', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101', 'c9f2b8d2-7a2b-4a0e-b7bc-0e1b34407dcb'),

-- Para Caixa Alfa (tenant 01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101)
('b68d8d30-3089-4e64-b3f6-c7f93e51afcc', 'origem-3', '002', '54321-0', '1', 'Conta 1 da Caixa Alfa', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101', 'a1d7b4e5-8f7c-4ed7-b1c2-9c3e6a19f8b0'),
('a4145d24-8d99-4fcf-a24f-22f15b5f8dbf', 'origem-4', '002', '54322-1', '2', 'Conta 2 da Caixa Alfa', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101', 'a1d7b4e5-8f7c-4ed7-b1c2-9c3e6a19f8b0'),

-- Para Banco Vitta (tenant 02c33f64-e027-4b30-8186-65a539d2fa51)
('58e4d7f7-6b84-4de6-9cc2-879f0d69a0c2', 'origem-5', '003', '11223-3', '4', 'Conta 1 do Banco Vitta', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51', 'f3bce827-529d-47bb-a08a-2c25a8b1c452'),
('b09d041a-febd-4d6d-a4e2-8cc8f377c8a9', 'origem-6', '003', '11224-4', '5', 'Conta 2 do Banco Vitta', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51', 'f3bce827-529d-47bb-a08a-2c25a8b1c452'),

-- Para Caixa Vitta (tenant 02c33f64-e027-4b30-8186-65a539d2fa51)
('6ec79d43-3f43-4d23-b944-c47e9c0f366e', 'origem-7', '004', '33211-0', '9', 'Conta 1 da Caixa Vitta', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51', '8cae395f-cb22-4278-91a6-9b3a276bcb5e'),
('391fce8f-39b1-4082-a570-9a65018a7d14', 'origem-8', '004', '33212-1', '0', 'Conta 2 da Caixa Vitta', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51', '8cae395f-cb22-4278-91a6-9b3a276bcb5e'),

-- Para Banco Transpeto (tenant 03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937)
('58c1a037-44b0-4de3-9a7a-423356e9a1dc', 'origem-9', '005', '22113-7', '3', 'Conta 1 do Banco Transpeto', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937', '04ee3d4a-fd5a-47c3-b935-9d9cbf2a7de1'),
('e2b28472-8c8b-44c1-985d-4eebf49194cc', 'origem-10', '005', '22114-8', '4', 'Conta 2 do Banco Transpeto', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937', '04ee3d4a-fd5a-47c3-b935-9d9cbf2a7de1'),

-- Para Caixa Transpeto (tenant 03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937)
('1c7707bb-2f8f-4a27-b2a5-fc343b68ca7a', 'origem-11', '006', '99887-6', '2', 'Conta 1 da Caixa Transpeto', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937', 'ed1b6a2c-e464-4f9e-a77e-4225ac8ed4a6'),
('44a417b7-9c21-4adf-b624-cf5564bb6a8e', 'origem-12', '006', '99888-7', '3', 'Conta 2 da Caixa Transpeto', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937', 'ed1b6a2c-e464-4f9e-a77e-4225ac8ed4a6'),

-- Para Banco Milenium (tenant 04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3)
('c8ec6f63-68ae-4b33-b1ae-6b18d1ce7e32', 'origem-13', '007', '76543-2', '6', 'Conta 1 do Banco Milenium', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3', '623d2fcb-3f8b-41a8-9880-3d4fca18a264'),
('e98460a9-1c08-4468-847a-76883a408c52', 'origem-14', '007', '76544-3', '7', 'Conta 2 do Banco Milenium', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3', '623d2fcb-3f8b-41a8-9880-3d4fca18a264'),

-- Para Caixa Milenium (tenant 04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3)
('5285ac18-241b-4ff7-b60c-4772c6f8a1b7', 'origem-15', '008', '23456-7', '8', 'Conta 1 da Caixa Milenium', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3', 'ac1f62ee-8a3f-4d4a-9d26-2123a90ec28f'),
('847a8c54-503f-4f4b-8fcb-35a6b245b89a', 'origem-16', '008', '23457-8', '9', 'Conta 2 da Caixa Milenium', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3', 'ac1f62ee-8a3f-4d4a-9d26-2123a90ec28f'),

-- Para Banco BioTech (tenant 05de129a-392b-4fa4-8a04-0cf8ec85cd81)
('56f7be6f-5bcf-4d27-8f0a-7ae9e8830618', 'origem-17', '009', '34567-9', '1', 'Conta 1 do Banco BioTech', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81', '770a3c6d-eaf2-40ad-bb63-4c1dfe32e847'),
('fd1a3f8d-22a2-4fbd-9757-b7f9e6a7de44', 'origem-18', '009', '34568-0', '2', 'Conta 2 do Banco BioTech', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81', '770a3c6d-eaf2-40ad-bb63-4c1dfe32e847'),

-- Para Caixa BioTech (tenant 05de129a-392b-4fa4-8a04-0cf8ec85cd81)
('24d0c11f-fc0d-45da-bb4b-33a0dfdf7332', 'origem-19', '010', '87654-3', '4', 'Conta 1 da Caixa BioTech', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81', '87c4d097-4110-44ab-81fa-1e2e4a1a7c38'),
('3c7e8e58-3f4e-4d35-91b4-8a7a8d7bfc78', 'origem-20', '010', '87655-4', '5', 'Conta 2 da Caixa BioTech', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81', '87c4d097-4110-44ab-81fa-1e2e4a1a7c38'),

-- Para Banco Solara (tenant 06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6)
('6d92ccf9-1a3d-4744-b329-7285d3c6bba3', 'origem-21', '011', '98765-4', '6', 'Conta 1 do Banco Solara', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6', '3de91e9b-4f9f-4c4f-9274-96e14533479d'),
('98a651f4-fd28-42bb-b9ae-2a345e7d1a87', 'origem-22', '011', '98766-5', '7', 'Conta 2 do Banco Solara', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6', '3de91e9b-4f9f-4c4f-9274-96e14533479d'),

-- Para Caixa Solara (tenant 06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6)
('4c3fa6d1-334f-4a18-8a39-7e04163ca5f1', 'origem-23', '012', '11111-1', '8', 'Conta 1 da Caixa Solara', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6', 'f9caa48b-cd6f-4f82-bc93-c2ed146993e4'),
('bd7d5b9b-59f7-4f96-8e3c-61b0c3c865ec', 'origem-24', '012', '11112-2', '9', 'Conta 2 da Caixa Solara', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6', 'f9caa48b-cd6f-4f82-bc93-c2ed146993e4'),

-- Para Banco Nova Era (tenant 07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3)
('849734b4-f18f-414f-8a0b-75f5c7d65051', 'origem-25', '013', '22222-3', '0', 'Conta 1 do Banco Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '429f67e8-4c3c-416e-9d7d-779ecce5a1f3'),
('fa15280c-468e-42ea-8f1d-56e462f8d0d7', 'origem-26', '013', '22223-4', '1', 'Conta 2 do Banco Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '429f67e8-4c3c-416e-9d7d-779ecce5a1f3');

INSERT INTO public.financeiro_contas (id, id_origem, agencia, conta, digito_verificador, descricao, data_criacao, tenant_id, instituicao_financeira_id) VALUES
-- Para Banco Nova Era (tenant 07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3)
('d77a9b21-5f3c-43f1-8bbd-3c4f71b8d2e9', 'origem-29', '1601', '10001-0', '1', 'Conta 1 do Banco Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '429f67e8-4c3c-416e-9d7d-779ecce5a1f3'),
('2e96c04a-5b71-4f52-9b8a-18fbe0f7a6db', 'origem-30', '1601', '10002-1', '2', 'Conta 2 do Banco Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '429f67e8-4c3c-416e-9d7d-779ecce5a1f3'),

-- Para Caixa Nova Era (tenant 07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3)
('1f2d9c7b-cbd9-4ccf-9ebd-32540a2d1bc3', 'origem-31', '1602', '20001-0', '3', 'Conta 1 da Caixa Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '0a6a3d4b-c788-4f3d-b4d9-204d43e20970'),
('02a4576f-5e5d-45c1-9fca-2f541c31b193', 'origem-32', '1602', '20002-1', '4', 'Conta 2 da Caixa Nova Era', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3', '0a6a3d4b-c788-4f3d-b4d9-204d43e20970'),

-- Para Banco Logitech (tenant 08c5f7e3-cad9-4f7e-9090-478cfb1ef72d)
('42a5d7f3-90a4-4df1-a020-7b1eb91a2638', 'origem-33', '1701', '30001-0', '5', 'Conta 1 do Banco Logitech', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d', 'f05a9a7f-4d63-48f8-bc8a-8f46a735674c'),
('e0b1d3a7-cf6e-4f9b-8a61-9a65ee5f4f4a', 'origem-34', '1701', '30002-1', '6', 'Conta 2 do Banco Logitech', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d', 'f05a9a7f-4d63-48f8-bc8a-8f46a735674c'),

-- Para Caixa Logitech (tenant 08c5f7e3-cad9-4f7e-9090-478cfb1ef72d)
('3e75578d-8629-4b61-b299-d8f4f22a54b0', 'origem-35', '1702', '40001-0', '7', 'Conta 1 da Caixa Logitech', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d', 'eb2359b7-7d7b-4c04-a6cd-d012e8faad66'),
('1a08a927-fb3d-4e8c-a0f6-71e44b71e862', 'origem-36', '1702', '40002-1', '8', 'Conta 2 da Caixa Logitech', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d', 'eb2359b7-7d7b-4c04-a6cd-d012e8faad66'),

-- Para Banco Mercatto (tenant 09e3d2ac-19e3-46a5-a9e5-f7761177233e)
('bb3a6dcf-634b-46d6-8e9b-9c7f5e238d6f', 'origem-37', '1801', '50001-0', '9', 'Conta 1 do Banco Mercatto', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e', 'e8b053b3-f8b2-4ae7-9c68-210a5c9a1d7e'),
('06a1eabb-299d-40df-9fcb-fc51ca2686ae', 'origem-38', '1801', '50002-1', '0', 'Conta 2 do Banco Mercatto', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e', 'e8b053b3-f8b2-4ae7-9c68-210a5c9a1d7e'),

-- Para Caixa Mercatto (tenant 09e3d2ac-19e3-46a5-a9e5-f7761177233e)
('1d742bd7-87b3-4f3c-b54f-2b7768b3b8ca', 'origem-39', '1802', '60001-0', '1', 'Conta 1 da Caixa Mercatto', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e', 'd7a9e61a-23ee-4d36-b4f5-3f1d4eae23bb'),
('6e1f8a12-23e8-463f-9b0a-6f68db0a9aee', 'origem-40', '1802', '60002-1', '2', 'Conta 2 da Caixa Mercatto', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e', 'd7a9e61a-23ee-4d36-b4f5-3f1d4eae23bb'),

-- Para Banco Vida e Saúde (tenant 10bbcf76-58ae-4b94-b391-dfa1546e2466)
('c1547ca2-c66c-4b8d-9c69-59cb0e6a3a0e', 'origem-41', '1901', '70001-0', '3', 'Conta 1 do Banco Vida e Saúde', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466', 'c84e04bb-32a3-4f9c-8cb4-7f1f9ac59b23'),
('f70f374d-5973-4c7f-9b48-418a6f7d8d2c', 'origem-42', '1901', '70002-1', '4', 'Conta 2 do Banco Vida e Saúde', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466', 'c84e04bb-32a3-4f9c-8cb4-7f1f9ac59b23'),

-- Para Caixa Vida e Saúde (tenant 10bbcf76-58ae-4b94-b391-dfa1546e2466)
('1a94f39f-118d-4451-9c84-ec785c6a7c32', 'origem-43', '1902', '80001-0', '5', 'Conta 1 da Caixa Vida e Saúde', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466', 'a3f95ca3-e418-4db0-88c4-102d1e2e9d7d'),
('07ab2f87-5b3b-4f12-bf9d-f209e39c4453', 'origem-44', '1902', '80002-1', '6', 'Conta 2 da Caixa Vida e Saúde', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466', 'a3f95ca3-e418-4db0-88c4-102d1e2e9d7d');

-- Produtos para tenant Alfa Indústria Metalúrgica Ltda. (01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101)
INSERT INTO public.produto_produtos 
(id, id_origem, referencia, descricao, grupo, id_grupo_origem, marca, id_marca_origem, gtin, ativo, data_criacao, tenant_id) VALUES
('7e6b0c26-49d4-42d7-9c33-3f9f1a82a6d7', 'prod-001', 'REF1001', 'Parafuso de aço inox 10mm', 'Fixadores', 'grp01', 'Metalúrgica Souza', 'marca01', '7891234560012', true, '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('e99c672a-bc2a-460d-888b-16c492e2bc44', 'prod-002', 'REF1002', 'Porca sextavada 10mm', 'Fixadores', 'grp01', 'Metalúrgica Souza', 'marca01', '7891234560013', true, '2023-04-01 09:05:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('0c60b3df-7ec5-4d5b-99de-8d9ca0f4c4e1', 'prod-003', 'REF1003', 'Chave de fenda 15cm', 'Ferramentas', 'grp02', 'Fornos Equip', 'marca02', '7891234560014', true, '2023-04-01 09:10:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('a8e7120a-e3a5-4c0a-b8f6-15b5a7975c6e', 'prod-004', 'REF1004', 'Martelo de borracha 500g', 'Ferramentas', 'grp02', 'Fornos Equip', 'marca02', '7891234560015', true, '2023-04-01 09:15:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('b68f32dc-5d4a-4f0d-b8d0-75edcdd99ff1', 'prod-005', 'REF1005', 'Lixa para madeira 100mm', 'Abrasivos', 'grp03', 'Ferros & Aços', 'marca03', '7891234560016', true, '2023-04-01 09:20:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('c9d95377-2ef6-4df4-bd75-8aef4de3df2d', 'prod-006', 'REF1006', 'Serra manual 12"', 'Ferramentas', 'grp02', 'Tecnomet', 'marca04', '7891234560017', true, '2023-04-01 09:25:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('7ca1e7ec-37ac-4c25-9ef2-9f049b4b9c8b', 'prod-007', 'REF1007', 'Fita isolante 20m', 'Elétricos', 'grp04', 'Indústrias Almeida', 'marca05', '7891234560018', true, '2023-04-01 09:30:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('2d17d96e-51b8-4e69-b1fa-1e781bfaa832', 'prod-008', 'REF1008', 'Conector elétrico', 'Elétricos', 'grp04', 'Indústrias Almeida', 'marca05', '7891234560019', true, '2023-04-01 09:35:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('e51f8d47-03ee-4b22-92e1-184e9f51a6d4', 'prod-009', 'REF1009', 'Bomba hidráulica 5HP', 'Máquinas', 'grp05', 'Tecnomet', 'marca04', '7891234560020', true, '2023-04-01 09:40:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('75eefa0b-f1f8-4a57-8b64-f3463248d040', 'prod-010', 'REF1010', 'Motor elétrico 220V', 'Máquinas', 'grp05', 'Tecnomet', 'marca04', '7891234560021', true, '2023-04-01 09:45:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101');

-- Produtos para tenant Grupo Vitta Serviços Corporativos (02c33f64-e027-4b30-8186-65a539d2fa51)
INSERT INTO public.produto_produtos 
(id, id_origem, referencia, descricao, grupo, id_grupo_origem, marca, id_marca_origem, gtin, ativo, data_criacao, tenant_id) VALUES
('3b14b52f-1e21-4a5a-931a-872b0a72df51', 'prod-101', 'VIT1001', 'Notebook Vitta Core i7 16GB', 'Informática', 'grp10', 'Vitta Equip', 'marca10', '7894561230012', true, '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('8a19f7bb-74d1-4c92-8c3a-d34d1a21e7f2', 'prod-102', 'VIT1002', 'Monitor LED 24"', 'Informática', 'grp10', 'Vitta Equip', 'marca10', '7894561230013', true, '2023-06-12 15:50:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('c7a10e8d-f8c9-44b3-bfcf-4c7a9d738d60', 'prod-103', 'VIT1003', 'Teclado mecânico RGB', 'Informática', 'grp10', 'Tech Vitta', 'marca11', '7894561230014', true, '2023-06-12 15:55:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('981b1437-7981-4a6a-a943-4a3206b713f7', 'prod-104', 'VIT1004', 'Mouse óptico USB', 'Informática', 'grp10', 'Tech Vitta', 'marca11', '7894561230015', true, '2023-06-12 16:00:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('bfe503c4-4346-4d6b-9e52-59c1b2e502c1', 'prod-105', 'VIT1005', 'Cadeira ergonômica escritório', 'Móveis', 'grp11', 'Vitta Serviços', 'marca12', '7894561230016', true, '2023-06-12 16:05:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('17d967cb-8a3f-47a3-bd6c-860051eaee63', 'prod-106', 'VIT1006', 'Mesa de reunião 1,80m', 'Móveis', 'grp11', 'Vitta Serviços', 'marca12', '7894561230017', true, '2023-06-12 16:10:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('e9b9fa4d-5ee8-4ee4-837d-1d158b2d9f3a', 'prod-107', 'VIT1007', 'Impressora laser A4', 'Equipamentos', 'grp12', 'Tech Vitta', 'marca11', '7894561230018', true, '2023-06-12 16:15:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('0f8f0a1e-b3a1-4177-9c5e-6f6e1d269efa', 'prod-108', 'VIT1008', 'Scanner documento', 'Equipamentos', 'grp12', 'Tech Vitta', 'marca11', '7894561230019', true, '2023-06-12 16:20:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('1a7ec11f-990b-4e0b-9d0f-01a8eec91adf', 'prod-109', 'VIT1009', 'Projetor multimídia', 'Equipamentos', 'grp12', 'Vitta Equip', 'marca10', '7894561230020', true, '2023-06-12 16:25:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('92a7425b-d55e-4c94-940d-fb6c2ff3bba9', 'prod-110', 'VIT1010', 'Estabilizador de energia 2000VA', 'Equipamentos', 'grp12', 'Vitta Equip', 'marca10', '7894561230021', true, '2023-06-12 16:30:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51');

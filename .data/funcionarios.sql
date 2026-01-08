-- Vendedores para todos os tenants listados

-- TOTVS Protheus Tenants

INSERT INTO public.funcionario_funcionarios (id, id_origem, nome, cpf, cnpj_loja, funcao, data_criacao, tenant_id) VALUES
-- Alfa Indústria Metalúrgica Ltda.
('a1e9f28a-c9b7-4b0a-b1cc-4b8c6d1a2b7e', 'origem-101', 'Carlos Silva', '12345678901', '12345678000190', 'Vendedor', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('b2d9e31f-3494-43dc-b932-7f8eab53d502', 'origem-102', 'Fernanda Souza', '98765432100', '12345678000190', 'Vendedor', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('c3f5a7e4-2218-4bf7-a2b5-0c9dba8d7a7f', 'origem-103', 'João Pereira', '19283746500', '12345678000190', 'Vendedor', '2023-04-01 09:00:00-03', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Grupo Vitta Serviços Corporativos
('d4b6c3d9-522a-4f9e-9c9d-14f1b9f33c15', 'origem-104', 'Aline Rodrigues', '11122233344', '98765432000101', 'Vendedor', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('e5c7f6a8-8e4f-4473-a987-6c8bdc5c2edb', 'origem-105', 'Ricardo Lima', '55566677788', '98765432000101', 'Vendedor', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('f6a1e3b7-3342-4a1d-8c75-92e3fb2c9e70', 'origem-106', 'Paula Fernandes', '99988877766', '98765432000101', 'Vendedor', '2023-06-12 15:45:00-03', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Transpeto Logística S.A.
('17e46d98-4b02-4b3a-9e35-1cbfdf0d6a45', 'origem-107', 'Thiago Santos', '66655544433', '15982374000166', 'Vendedor', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937'),
('28f57e6b-6d79-45b8-a77a-bfc4a44edc0f', 'origem-108', 'Camila Alves', '77788899900', '15982374000166', 'Vendedor', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937'),
('39968a0d-0513-4eae-bd4a-2a65a0d9f127', 'origem-109', 'Bruno Costa', '22233344455', '15982374000166', 'Vendedor', '2023-08-20 10:30:00-03', '03f1c4a5-9b87-44ce-bdbe-9d2d5e14a937'),

-- Milenium Engenharia e Construção Ltda.
('4a0c7f51-8e1d-4d6c-b57a-0c0d6c124e6f', 'origem-110', 'Mariana Nunes', '12312312399', '63487159000132', 'Vendedor', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3'),
('5b1d8a62-9f2e-4b7d-ada2-2398d6f4d5d2', 'origem-111', 'Eduardo Martins', '45645645688', '63487159000132', 'Vendedor', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3'),
('6c2e9b73-af3f-4c8e-b30d-45f6d72c8a77', 'origem-112', 'Isabela Rocha', '78978978977', '63487159000132', 'Vendedor', '2024-01-11 11:15:00-03', '04abcfd2-79e1-4fc6-9d51-1a2a8b9b43a3'),

-- BioTech Farmacêutica S.A.
('7d3fab84-cf5b-41a9-963c-5c7bd9085e99', 'origem-113', 'Renato Lima', '32132132111', '70987321000184', 'Vendedor', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81'),
('8e4fbc95-df6c-42bb-8a55-9a49e0a77c3a', 'origem-114', 'Luciana Gomes', '65465465422', '70987321000184', 'Vendedor', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81'),
('9f50cd06-ea7d-443c-b5a6-7b70e4f99d83', 'origem-115', 'Fábio Almeida', '98798798733', '70987321000184', 'Vendedor', '2023-10-05 14:00:00-03', '05de129a-392b-4fa4-8a04-0cf8ec85cd81'),

-- SAP Business One Tenants

-- Solara Energia Renovável Ltda.
('a0615d27-2e77-4f8a-9319-0ea9b30d8f40', 'origem-116', 'Daniela Castro', '11122233344', '44123456000110', 'Vendedor', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6'),
('b1726e38-3f88-4939-bfcb-7dc4e490aeab', 'origem-117', 'Gabriel Melo', '55566677788', '44123456000110', 'Vendedor', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6'),
('c2837f49-4b99-4adf-9c45-9e5e1c03e74e', 'origem-118', 'Patrícia Rocha', '99988877766', '44123456000110', 'Vendedor', '2022-12-05 08:30:00-03', '06bd4f03-0fc6-462c-a647-e6a2bc5e9ea6'),

-- Nova Era Têxtil Ltda.
('d39480fa-5a0a-46bd-9227-8e5b1b9b5fdd', 'origem-119', 'Marcos Vinícius', '66655544433', '33654987000144', 'Vendedor', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3'),
('e4a5921b-6b0b-45cc-93db-7f8d3f8a6c4c', 'origem-120', 'Renata Moreira', '77788899900', '33654987000144', 'Vendedor', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3'),
('f5b6a32c-7c1c-4d7e-a761-2c2e9d2b7c44', 'origem-121', 'Vinícius Silva', '22233344455', '33654987000144', 'Vendedor', '2023-02-15 09:50:00-03', '07ef32b8-431e-4ed4-a5d3-8dd830b9d0b3'),

-- Logitech Transportes Ltda.
('a6c7b43d-8d2d-4b85-94ea-3f8e2a4f9b3f', 'origem-122', 'Amanda Farias', '12312312399', '27444888000112', 'Vendedor', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d'),
('b7d8c54e-9e3e-4c96-a8b7-7c8e7f6f5f22', 'origem-123', 'Felipe Andrade', '45645645688', '27444888000112', 'Vendedor', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d'),
('c8e9d65f-af4f-4da7-bc58-3a3b6f1e4f88', 'origem-124', 'Bianca Lima', '78978978977', '27444888000112', 'Vendedor', '2023-04-28 17:20:00-03', '08c5f7e3-cad9-4f7e-9090-478cfb1ef72d'),

-- Mercatto Varejo Inteligente Ltda.
('d9fae76a-b05c-4128-8c8f-0d0c5e9a7a9e', 'origem-125', 'Lucas Fernandes', '32132132111', '19999333000166', 'Vendedor', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e'),
('ea0b087b-c16d-4b39-a6f5-1f6a2c3b8a7f', 'origem-126', 'Patrícia Costa', '65465465422', '19999333000166', 'Vendedor', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e'),
('fb1c198c-d27e-43a2-b75a-7b8c4f9e2f34', 'origem-127', 'Marcio Oliveira', '98798798733', '19999333000166', 'Vendedor', '2023-07-09 13:40:00-03', '09e3d2ac-19e3-46a5-a9e5-f7761177233e'),

-- Clínica Médica Vida e Saúde S.A.
('0c2d2a9d-e38f-4f6c-bd99-0f9c4e5f2a1a', 'origem-128', 'Renata Moura', '11122233344', '88222555000177', 'Vendedor', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466'),
('1d3e3b0e-f49a-4a7d-99db-1e0d5f6e3b2b', 'origem-129', 'Igor Santos', '55566677788', '88222555000177', 'Vendedor', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466'),
('2e4f4c1f-05ab-4b8e-8ac1-2f1e6f7f4c3c', 'origem-130', 'Sônia Ribeiro', '99988877766', '88222555000177', 'Vendedor', '2023-09-21 08:05:00-03', '10bbcf76-58ae-4b94-b391-dfa1546e2466');

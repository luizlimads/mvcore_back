-- Categorias para tenant Alfa Indústria Metalúrgica Ltda.

INSERT INTO public.financeiro_categorias (id, id_origem, descricao, tipo, data_criacao, categoria_pai_id, tenant_id) VALUES
('cb1a3f70-4a29-4a64-9b3b-1bca37d3f2e0', 'cat-001', 'Receitas Operacionais', 'Entradas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('d7e6b349-2f8e-4f5f-95f3-7ab9bde364db', 'cat-002', 'Receitas Não Operacionais', 'Entradas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('0f14ac1d-3d22-4b87-bdb0-2be78b5a4770', 'cat-003', 'Despesas Operacionais', 'Saídas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('aa92db6a-c3e6-446e-b80f-d7e040f7d99f', 'cat-004', 'Despesas Financeiras', 'Saídas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('23fa4f20-f38e-4b3a-8e5c-4bc7f4f94975', 'cat-005', 'Investimentos', 'Saídas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Subcategorias Receita Operacionais
('c88e56a3-79cb-4a1f-bd62-59f7b32a6c6f', 'cat-006', 'Vendas de Produtos', 'Entradas', '2023-04-01 09:00:00-03', 'cb1a3f70-4a29-4a64-9b3b-1bca37d3f2e0', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('f46c2899-4d16-4a62-bf35-87a5e3e983ab', 'cat-007', 'Serviços Prestados', 'Entradas', '2023-04-01 09:00:00-03', 'cb1a3f70-4a29-4a64-9b3b-1bca37d3f2e0', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Subcategorias Receita Não Operacionais
('2871b8c7-3c39-4e43-9204-6f68f841a56d', 'cat-008', 'Juros Recebidos', 'Entradas', '2023-04-01 09:00:00-03', 'd7e6b349-2f8e-4f5f-95f3-7ab9bde364db', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('46f01c4f-6d81-49f6-9f4a-caf3a8f59b1a', 'cat-009', 'Venda de Ativos', 'Entradas', '2023-04-01 09:00:00-03', 'd7e6b349-2f8e-4f5f-95f3-7ab9bde364db', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Subcategorias Despesas Operacionais
('d3e7f7b3-b4c6-4799-bcbb-38d7e5d0a568', 'cat-010', 'Salários e Ordenados', 'Saídas', '2023-04-01 09:00:00-03', '0f14ac1d-3d22-4b87-bdb0-2be78b5a4770', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('fbf9c88b-0d05-4a99-8744-3f14c32b78a3', 'cat-011', 'Aluguel', 'Saídas', '2023-04-01 09:00:00-03', '0f14ac1d-3d22-4b87-bdb0-2be78b5a4770', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('1e1a9538-1b0f-4260-a3e6-7b9f35b06374', 'cat-012', 'Energia Elétrica', 'Saídas', '2023-04-01 09:00:00-03', '0f14ac1d-3d22-4b87-bdb0-2be78b5a4770', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Subcategorias Despesas Financeiras
('a4f7a1a5-f4ca-4f25-bd9b-11791d55edbc', 'cat-013', 'Juros Pagos', 'Saídas', '2023-04-01 09:00:00-03', 'aa92db6a-c3e6-446e-b80f-d7e040f7d99f', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('8d0842e1-6dd9-463f-80ae-59f04d810d0e', 'cat-014', 'Taxas Bancárias', 'Saídas', '2023-04-01 09:00:00-03', 'aa92db6a-c3e6-446e-b80f-d7e040f7d99f', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Subcategoria Investimentos
('f8337a3d-e3a5-4d99-b6a3-b4f5a3b90ef7', 'cat-015', 'Compra de Equipamentos', 'Saídas', '2023-04-01 09:00:00-03', '23fa4f20-f38e-4b3a-8e5c-4bc7f4f94975', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('963b2768-4e81-46e8-9ee0-6911cb3a8a40', 'cat-016', 'Pesquisa e Desenvolvimento', 'Saídas', '2023-04-01 09:00:00-03', '23fa4f20-f38e-4b3a-8e5c-4bc7f4f94975', '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),

-- Outras categorias avulsas
('33c642bb-0994-4629-90c3-e8005f1a8a15', 'cat-017', 'Despesas com Marketing', 'Saídas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('18d15147-81b1-49aa-99d6-0d034f290aa8', 'cat-018', 'Receita de Aluguéis', 'Entradas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('30e73217-5fc3-4ca0-8b62-27ed7a29f47f', 'cat-019', 'Despesas com Transporte', 'Saídas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101'),
('e01990d3-f75f-48a3-a865-f522c4d06c3a', 'cat-020', 'Receita de Serviços', 'Entradas', '2023-04-01 09:00:00-03', NULL, '01eaae23-cf0d-4b15-a6f4-8f3a5c6fc101');




-- Categorias para tenant Grupo Vitta Serviços Corporativos

INSERT INTO public.financeiro_categorias (id, id_origem, descricao, tipo, data_criacao, categoria_pai_id, tenant_id) VALUES
('8b9b2908-509b-411b-8e36-1d6b2a1972bf', 'cat-101', 'Receitas Operacionais', 'Entradas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51'),
('ba10a2cd-cfe6-4d70-b21d-013313d58508', 'cat-102', 'Receitas Não Operacionais', 'Entradas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51'),
('2b7f7d9e-c095-4de2-b4eb-93c1f6a4ca01', 'cat-103', 'Despesas Operacionais', 'Saídas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51'),
('0e0b2414-8f99-49b9-94e6-b3e9d43e932c', 'cat-104', 'Despesas Financeiras', 'Saídas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51'),
('0e5e6e17-0cb7-4f0f-9bb2-f812b23d3e06', 'cat-105', 'Investimentos', 'Saídas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Subcategorias Receita Operacionais
('54f7dd38-77b3-4c7f-8a4a-16b8a676607b', 'cat-106', 'Vendas de Produtos', 'Entradas', '2023-06-12 15:45:00-03', '8b9b2908-509b-411b-8e36-1d6b2a1972bf', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('a52d2d42-ec4c-4b0a-baf6-2c564b214840', 'cat-107', 'Serviços Prestados', 'Entradas', '2023-06-12 15:45:00-03', '8b9b2908-509b-411b-8e36-1d6b2a1972bf', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Subcategorias Receita Não Operacionais
('0d69b44f-80a0-4dd0-a2be-41a56ed010b6', 'cat-108', 'Juros Recebidos', 'Entradas', '2023-06-12 15:45:00-03', 'ba10a2cd-cfe6-4d70-b21d-013313d58508', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('8f012f12-f87a-40c9-9b65-1e8700fce53c', 'cat-109', 'Venda de Ativos', 'Entradas', '2023-06-12 15:45:00-03', 'ba10a2cd-cfe6-4d70-b21d-013313d58508', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Subcategorias Despesas Operacionais
('1444d0d5-c5e4-4ac8-9fa9-9cc0e5ad6a2c', 'cat-110', 'Salários e Ordenados', 'Saídas', '2023-06-12 15:45:00-03', '2b7f7d9e-c095-4de2-b4eb-93c1f6a4ca01', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('c3b61a7a-5c0a-4568-b8bb-d5020d9e3e90', 'cat-111', 'Aluguel', 'Saídas', '2023-06-12 15:45:00-03', '2b7f7d9e-c095-4de2-b4eb-93c1f6a4ca01', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('88c70d4c-2407-4460-a868-5c0b4f591e68', 'cat-112', 'Energia Elétrica', 'Saídas', '2023-06-12 15:45:00-03', '2b7f7d9e-c095-4de2-b4eb-93c1f6a4ca01', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Subcategorias Despesas Financeiras
('7e41f74a-3508-4322-8479-9398d3034e2d', 'cat-113', 'Juros Pagos', 'Saídas', '2023-06-12 15:45:00-03', '0e0b2414-8f99-49b9-94e6-b3e9d43e932c', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('b204f22a-40ed-4411-b8b3-33b3144f8a72', 'cat-114', 'Taxas Bancárias', 'Saídas', '2023-06-12 15:45:00-03', '0e0b2414-8f99-49b9-94e6-b3e9d43e932c', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Subcategoria Investimentos
('f99f8e72-b56c-4b44-8db6-4b112d4bf26c', 'cat-115', 'Compra de Equipamentos', 'Saídas', '2023-06-12 15:45:00-03', '0e5e6e17-0cb7-4f0f-9bb2-f812b23d3e06', '02c33f64-e027-4b30-8186-65a539d2fa51'),
('da6b48a5-e95e-4f4b-99c4-25b31d92a7c6', 'cat-116', 'Pesquisa e Desenvolvimento', 'Saídas', '2023-06-12 15:45:00-03', '0e5e6e17-0cb7-4f0f-9bb2-f812b23d3e06', '02c33f64-e027-4b30-8186-65a539d2fa51'),

-- Outras categorias avulsas
('d4227898-f91e-4eb3-8f93-6809327a7d94', 'cat-117', 'Despesas com Marketing', 'Saídas', '2023-06-12 15:45:00-03', NULL, '02c33f64-e027-4b30-8186-65a539d2fa51');

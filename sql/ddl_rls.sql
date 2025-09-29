-- EXTENSIONS
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- PRODUCTS
create table if not exists public.products (
  id varchar(50) primary key,
  name varchar(255) not null,
  brand varchar(100) not null,
  category varchar(100) not null,
  images jsonb not null,
  price numeric(12,2) not null,
  discount int not null default 0,
  rating real not null default 0,
  review_count int not null default 0,
  sold_count int not null default 0,
  created_at timestamptz not null default now()
);

create index if not exists idx_products_brand on public.products(brand);
create index if not exists idx_products_category on public.products(category);
create index if not exists idx_products_rating on public.products(rating);
create index if not exists idx_products_sold on public.products(sold_count);

alter table public.products enable row level security;

-- Allow read to everyone
drop policy if exists products_select_public on public.products;
create policy products_select_public
on public.products for select
to anon, authenticated
using (true);

-- Admin write (uses JWT custom claim "role")
drop policy if exists products_write_admin on public.products;
create policy products_write_admin
on public.products for all
to authenticated
using ( (auth.jwt() ->> 'role') = 'admin' )
with check ( (auth.jwt() ->> 'role') = 'admin' );

-- CART
create table if not exists public.cart (
  cart_id bigserial primary key,
  user_id uuid not null,
  product_id varchar(50) not null references public.products(id) on delete cascade,
  quantity int not null check (quantity > 0),
  created_at timestamptz not null default now(),
  unique (user_id, product_id)
);

create index if not exists idx_cart_user on public.cart(user_id);

alter table public.cart enable row level security;

-- Owner can select/insert/update/delete own cart rows
drop policy if exists cart_owner_select on public.cart;
create policy cart_owner_select
on public.cart for select
to authenticated
using (user_id = auth.uid());

drop policy if exists cart_owner_insert on public.cart;
create policy cart_owner_insert
on public.cart for insert
to authenticated
with check (user_id = auth.uid());

drop policy if exists cart_owner_update on public.cart;
create policy cart_owner_update
on public.cart for update
to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

drop policy if exists cart_owner_delete on public.cart;
create policy cart_owner_delete
on public.cart for delete
to authenticated
using (user_id = auth.uid());

-- ORDERS
create table if not exists public.orders (
  order_id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  total_price numeric(12,2) not null check (total_price >= 0),
  status text not null default 'pending' check (status in ('pending','paid','delivered')),
  created_at timestamptz not null default now()
);

create index if not exists idx_orders_user on public.orders(user_id);
create index if not exists idx_orders_status on public.orders(status);

alter table public.orders enable row level security;

-- Owner can read their orders
drop policy if exists orders_owner_select on public.orders;
create policy orders_owner_select
on public.orders for select
to authenticated
using (user_id = auth.uid());

-- Owner can insert their orders
drop policy if exists orders_owner_insert on public.orders;
create policy orders_owner_insert
on public.orders for insert
to authenticated
with check (user_id = auth.uid());

-- Only admin can update status or delete
drop policy if exists orders_admin_update on public.orders;
create policy orders_admin_update
on public.orders for update
to authenticated
using ( (auth.jwt() ->> 'role') = 'admin' )
with check ( (auth.jwt() ->> 'role') = 'admin' );

drop policy if exists orders_admin_delete on public.orders;
create policy orders_admin_delete
on public.orders for delete
to authenticated
using ( (auth.jwt() ->> 'role') = 'admin' );

-- ADDRESSES
create table if not exists public.addresses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  label text not null,
  receiver_name text not null,
  phone text not null,
  address_line text not null,
  city text not null,
  province text not null,
  postal_code text not null,
  is_default boolean default false,
  created_at timestamptz not null default now()
);

create index if not exists idx_addresses_user on public.addresses(user_id);

alter table public.addresses enable row level security;

-- Owner can select/insert/update/delete own addresses
drop policy if exists addresses_owner_select on public.addresses;
create policy addresses_owner_select
on public.addresses for select
to authenticated
using (user_id = auth.uid());

drop policy if exists addresses_owner_insert on public.addresses;
create policy addresses_owner_insert
on public.addresses for insert
to authenticated
with check (user_id = auth.uid());

drop policy if exists addresses_owner_update on public.addresses;
create policy addresses_owner_update
on public.addresses for update
to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());

drop policy if exists addresses_owner_delete on public.addresses;
create policy addresses_owner_delete
on public.addresses for delete
to authenticated
using (user_id = auth.uid());

-- Add address_id column to orders table after addresses table is created
alter table public.orders add column if not exists address_id uuid references public.addresses(id);

-- ORDER ITEMS
create table if not exists public.order_items (
  id bigserial primary key,
  order_id uuid not null references public.orders(order_id) on delete cascade,
  product_id varchar(50) not null references public.products(id) on delete restrict,
  quantity int not null check (quantity > 0),
  price numeric(12,2) not null check (price >= 0),
  subtotal numeric(12,2) generated always as (price * quantity) stored
);

create index if not exists idx_order_items_order on public.order_items(order_id);
create index if not exists idx_order_items_product on public.order_items(product_id);

alter table public.order_items enable row level security;

-- Only owner of the order can view their order items
drop policy if exists order_items_owner_select on public.order_items;
create policy order_items_owner_select
on public.order_items for select
to authenticated
using (
  order_id in (
    select order_id from public.orders where user_id = auth.uid()
  )
);

-- Allow insert order items only if the order belongs to the current user
drop policy if exists order_items_owner_insert on public.order_items;
create policy order_items_owner_insert
on public.order_items for insert
to authenticated
with check (
  order_id in (
    select order_id from public.orders where user_id = auth.uid()
  )
);

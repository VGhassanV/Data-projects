--Orders tables 

SELECT
	o.order_id,
	i.item_price,
	o.quantity,
	i.item_cat,
	i.item_name,
	o.created_at,
	a.delivery_address1,
	a.delivery_address2,
	a.delivery_city,
	a.delivery_zipcode,
	o.delivery 
FROM
	orders o
	LEFT JOIN items i ON o.item_id = i.item_id
	LEFT JOIN address a ON o.add_id = a.add_id;

--Inventory Managment
--section 1 

SELECT
	o.item_id,
	i.sku,
	i.item_name,
	SUM( o.quantity ) AS order_quantity,
	r.quantity AS recipe_quantity,
	ing.ing_name AS ingredient,
	( ing.ing_price / ing.ing_weight ) AS unit_cost,
	(
	r.quantity * SUM( o.quantity )) AS ordered_weight,
	( ing.ing_price / ing.ing_weight ) * (
	r.quantity * SUM( o.quantity )) AS ingredient_cost 
FROM
	orders o
	LEFT JOIN items i ON o.item_id = i.item_id
	LEFT JOIN recipie r ON i.sku = r.recipie_id
	LEFT JOIN ingredients ing ON r.ing_id = ing.ing_id 
GROUP BY
	o.item_id,
	i.sku,
	i.item_name,
	r.ing_id,
	r.quantity;

--Inventory Managment
--Section 2 

SELECT
	s1.ing_id,
	s1.ingredient,
	total_ordered_weight,
	( inv.quantity * ing.ing_weight ) AS total_inv_weight,
	( inv.quantity * ing.ing_weight ) - total_ordered_weight AS available_inv 
FROM
	( SELECT ing_id, ingredient, SUM( ordered_quantity ) AS total_ordered_weight FROM `stock 1` GROUP BY ingredient, ing_id ) s1
	LEFT JOIN inventory inv ON inv.item_id = s1.ing_id
	LEFT JOIN ingredients ing ON s1.ing_id = ing.ing_id;

--Staff Managment 

SELECT
	r.date, 
	s.firs_name as first_name,
	s.last_name,
	s.hourly_rate,
	sh.start_time,
	sh.end_time, 
	((HOUR(TIMEDIFF(sh.end_time,sh.start_time))*60) + (MINUTE(TIMEDIFF(sh.end_time,sh.start_time))))/60 as total_hours,
	(((HOUR(TIMEDIFF(sh.end_time,sh.start_time))*60) + (MINUTE(TIMEDIFF(sh.end_time,sh.start_time))))/60)*s.hourly_rate as labor_cost
	
FROM
	rotation r
	LEFT JOIN staff s ON r.staff_id = s.staff_id
	LEFT JOIN shifts sh ON r.shift_id = sh.shift_id;
	
	
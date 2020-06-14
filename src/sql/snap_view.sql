create view snap as
    select
        date
        ,state_id
         ,store_id
        ,case
            when state_id ='CA' then snap_ca
            when state_id ='WI' then snap_tx
            when state_id ='TX' then snap_tx
            end
        as snap


from calendar
full outer join (select distinct store_id, state_id from item_info)

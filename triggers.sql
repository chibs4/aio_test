create or replace function update_timestamps_after_object_insert() returns trigger as $$
declare --Переменные
    image_id uuid;
    dataset_id uuid;
    dix_id uuid;
    task_id uuid;
begin
    -- Получение нужных id
    select o.image, o.dataset into image_id, dataset_id from objects o where id = new.id;
    select dix.id into dix_id from dataset_image_xrefs dix where image=image_id and dataset=dataset_id;
    select d.task into task_id from datasets d where id = dataset_id;
    -- Операции обновления. Везде будет одно и то же время
    update dataset_image_xrefs set updated_datetime = now() where id = dix_id;
    update datasets set updated_datetime = now() where id = dataset_id;
    update tasks set last_change_datetime = now() where id = task_id;
    return null;
end;
$$ language plpgsql;

-- Триггер, который обновляет tasks, dataset, image updated_at при добавлении объектов на изображение
drop trigger if exists update_timestamps_after_object_insert on objects;
create trigger update_timestamps_after_object_insert
after insert on objects
for each row execute procedure update_timestamps_after_object_insert();


create or replace function update_tasks_timestamp() returns trigger as $func$
begin
    --Операция обновления задачи по id
    if tg_op = 'DELETE' then
        update tasks set last_change_datetime = now() where id = old.task;
        return old;
    elsif tg_op = 'INSERT' then
        update tasks set last_change_datetime = now() where id = new.task;
        return new;
    end if;
end;
$func$ language plpgsql;

-- Триггер, который обновляет tasks updated_at при добавлении строки в task_executor_xrefs
drop trigger if exists update_task_from_executor_update on task_executor_xrefs;
create trigger update_task_from_executor_update
before insert or delete on task_executor_xrefs
for each row execute procedure update_tasks_timestamp();


CREATE FUNCTION update_dataset_names_after_task_name_update()
RETURNS trigger AS $update_dataset_names_after_task_name_update$
BEGIN
    UPDATE datasets
    SET name = SPLIT_PART(name, '.', 1) || '. ' || NEW.name
    WHERE task = OLD.id;
    RETURN NULL;
END;
$update_dataset_names_after_task_name_update$ LANGUAGE plpgsql;

CREATE TRIGGER update_dataset_names_after_task_name_update
AFTER UPDATE OF name ON tasks
FOR EACH ROW EXECUTE PROCEDURE update_dataset_names_after_task_name_update();

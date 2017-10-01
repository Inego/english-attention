copy sentence from 'sentences.csv' with (FORMAT csv, DELIMITER '	', QUOTE E'\f');
copy list_sentence from 'sentences_in_lists.csv' with (FORMAT csv, DELIMITER '	', QUOTE E'\f');

insert into list_907 (text)
select
text
from sentence
where id in (select sentence from list_sentence where list = 907)
order by id
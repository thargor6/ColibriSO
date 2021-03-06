package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.frontend.dto.TagDto;
import org.mapstruct.Mapper;

@Mapper
public interface TagMapper {
  Tag dtoToEntiy(TagDto dto);

  TagDto entityToDto(Tag entity);
}

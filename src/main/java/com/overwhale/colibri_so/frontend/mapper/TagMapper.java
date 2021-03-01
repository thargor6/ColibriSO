package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.frontend.dto.TagDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TagMapper {
  TagMapper INSTANCE = Mappers.getMapper(TagMapper.class);

  Tag dtoToEntiy(TagDto dto);

  TagDto entityToDto(Tag entity);
}

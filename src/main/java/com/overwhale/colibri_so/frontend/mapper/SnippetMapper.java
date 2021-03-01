package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.dto.UserDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SnippetMapper {
  SnippetMapper INSTANCE = Mappers.getMapper(SnippetMapper.class);

  Snippet dtoToEntiy(SnippetDto dto);

  SnippetDto entityToDto(Snippet entity);
}

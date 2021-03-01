package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.SnippetTag;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.dto.SnippetTagDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SnippetTagMapper {
  SnippetTagMapper INSTANCE = Mappers.getMapper(SnippetTagMapper.class);

  SnippetTag dtoToEntiy(SnippetTagDto dto);

  SnippetTagDto entityToDto(SnippetTag entity);
}

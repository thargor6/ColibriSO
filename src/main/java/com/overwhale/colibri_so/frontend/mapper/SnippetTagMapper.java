package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.SnippetTag;
import com.overwhale.colibri_so.frontend.dto.SnippetTagDto;
import org.mapstruct.Mapper;

@Mapper
public interface SnippetTagMapper {
  SnippetTag dtoToEntiy(SnippetTagDto dto);

  SnippetTagDto entityToDto(SnippetTag entity);
}

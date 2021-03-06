package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import org.mapstruct.Mapper;

@Mapper
public interface SnippetMapper {
  Snippet dtoToEntiy(SnippetDto dto);

  SnippetDto entityToDto(Snippet entity);
}

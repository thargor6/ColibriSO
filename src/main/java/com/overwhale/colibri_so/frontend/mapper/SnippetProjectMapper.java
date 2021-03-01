package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.SnippetProject;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.dto.SnippetProjectDto;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SnippetProjectMapper {
  SnippetProjectMapper INSTANCE = Mappers.getMapper(SnippetProjectMapper.class);

  SnippetProject dtoToEntiy(SnippetProjectDto dto);

  SnippetProjectDto entityToDto(SnippetProject entity);
}

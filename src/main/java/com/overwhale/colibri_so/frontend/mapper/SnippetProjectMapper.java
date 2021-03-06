package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.SnippetProject;
import com.overwhale.colibri_so.frontend.dto.SnippetProjectDto;
import org.mapstruct.Mapper;

@Mapper
public interface SnippetProjectMapper {
  SnippetProject dtoToEntiy(SnippetProjectDto dto);

  SnippetProjectDto entityToDto(SnippetProject entity);
}

package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import com.overwhale.colibri_so.frontend.dto.SnippetIntentDto;
import org.mapstruct.Mapper;

@Mapper
public interface SnippetIntentMapper {
  SnippetIntent dtoToEntiy(SnippetIntentDto dto);

  SnippetIntentDto entityToDto(SnippetIntent entity);
}
